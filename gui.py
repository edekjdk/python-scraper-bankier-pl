import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class StockApp(tk.Tk):
    def __init__(self, data_path="data/data2.csv"):
        super().__init__()
        self.title("WIG20 Intraday Analyzer")
        self.geometry("1200x800")

        if not os.path.exists(data_path):
            self.show_error("Plik danych nie istnieje. Najpierw zescrapuj dane.")
            return

        self.df = pd.read_csv(data_path)
        self.df['Datetime'] = pd.to_datetime(self.df['Data'] + ' ' + self.df['Godzina'])
        self.df.sort_values(['Ticker', 'Datetime'], inplace=True)
        self.df['Return'] = self.df.groupby('Ticker')['Cena'].pct_change() * 100
        self.df['Hour'] = self.df['Datetime'].dt.hour
        self.df['Spread'] = self.df['Max 1D'] - self.df['Min 1D']
        self.df['VolumeDelta'] = self.df.groupby('Ticker')['Wolumen obrotu'].diff()
        self.df['Datetime_5min'] = self.df['Datetime'].dt.floor("5min")
        self.df['Return_5min'] = self.df.groupby('Ticker')['Cena'].pct_change() * 100

        self.tickers = sorted(self.df['Ticker'].unique())
        self.dates = sorted(self.df['Data'].unique())

        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Label(ctrl_frame, text="Spółka:").pack(side=tk.LEFT, padx=5)
        self.ticker_cb = ttk.Combobox(ctrl_frame, values=self.tickers, state="readonly")
        self.ticker_cb.current(0)
        self.ticker_cb.pack(side=tk.LEFT)

        ttk.Label(ctrl_frame, text="Dzień:").pack(side=tk.LEFT, padx=5)
        self.date_cb = ttk.Combobox(ctrl_frame, values=self.dates, state="readonly")
        self.date_cb.current(0)
        self.date_cb.pack(side=tk.LEFT)

        self.ticker_cb.bind("<<ComboboxSelected>>", lambda e: self.update_plots())
        self.date_cb.bind("<<ComboboxSelected>>", lambda e: self.update_plots())

        self.fig, self.axes = plt.subplots(2, 3, figsize=(12, 8), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.update_plots()

    def update_plots(self):
        ticker = self.ticker_cb.get()
        day = self.date_cb.get()

        sub = self.df[(self.df['Ticker'] == ticker) & (self.df['Data'] == day)]
        sub_all = self.df[self.df['Data'] == day]

        self.axes[0, 0].clear()
        self.axes[0, 0].plot(sub['Datetime'], sub['Cena'], marker='o')
        self.axes[0, 0].set_title('Cena intraday')

        self.axes[0, 1].clear()
        self.axes[0, 1].scatter(sub['Return'], sub['Wolumen obrotu'])
        self.axes[0, 1].set_title('Return vs Volume')

        self.axes[0, 2].clear()
        sub_box = sub.copy()
        sub_box['Hour'] = sub_box['Datetime'].dt.hour
        sub_box.boxplot(column='Return', by='Hour', ax=self.axes[0, 2])
        self.axes[0, 2].set_title('Boxplot: Return by Hour')
        self.axes[0, 2].figure.suptitle('')

        self.axes[1, 0].clear()
        pivot = sub_all.pivot_table(index='Datetime_5min', columns='Ticker', values='Return_5min')
        corr = pivot.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, cmap="coolwarm", annot=True, fmt=".2f", ax=self.axes[1, 0])
        self.axes[1, 0].set_title('Heatmap korelacji (5 min)')

        self.axes[1, 1].clear()
        self.axes[1, 1].plot(sub['Datetime'], sub['Spread'], marker='o')
        self.axes[1, 1].set_title('Spread over time')

        self.axes[1, 2].clear()
        vol_hour = sub.groupby(sub['Hour'])['VolumeDelta'].sum()
        self.axes[1, 2].plot(vol_hour.index, vol_hour.values, marker='o')
        self.axes[1, 2].set_title('Volume Delta by Hour')

        for ax in self.axes.flatten():
            ax.tick_params(axis='x', rotation=45)

        self.fig.suptitle(f"Analiza: {ticker} - {day}", fontsize=14)
        self.canvas.draw()

    def show_error(self, message):
        err_window = tk.Toplevel(self)
        err_window.title("Błąd")
        err_label = ttk.Label(err_window, text=message, foreground="red")
        err_label.pack(padx=20, pady=20)
        close_btn = ttk.Button(err_window, text="Zamknij", command=self.destroy)
        close_btn.pack(pady=10)

if __name__ == '__main__':
    app = StockApp()
    app.mainloop()
