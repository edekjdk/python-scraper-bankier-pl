import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class StockApp(tk.Tk):
    def __init__(window, data_path="data/data2.csv"):
        super().__init__()
        window.title("Wykresy spółek WIG20")
        window.geometry("1200x800")
        

        if not os.path.exists(data_path):
            window.show_error("Plik danych nie istnieje. Najpierw zescrapuj dane.")
            return

        window.df = pd.read_csv(data_path)
        window.df['Datetime'] = pd.to_datetime(window.df['Data'] + ' ' + window.df['Godzina'])
        window.df.sort_values(['Ticker', 'Datetime'], inplace=True)
        window.df['Return'] = window.df.groupby('Ticker')['Cena'].pct_change() * 100
        window.df['Hour'] = window.df['Datetime'].dt.hour
        window.df['Spread'] = window.df['Max 1D'] - window.df['Min 1D']
        window.df['VolumeDelta'] = window.df.groupby('Ticker')['Wolumen obrotu'].diff()
        window.df['Datetime_5min'] = window.df['Datetime'].dt.floor("5min")
        window.df['Return_5min'] = window.df.groupby('Ticker')['Cena'].pct_change() * 100

        window.tickers = sorted(window.df['Ticker'].unique())
        window.dates = sorted(window.df['Data'].unique())

        panel_ctrl = ttk.Frame(window)
        panel_ctrl.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Label(panel_ctrl, text="Spółka:").pack(side=tk.LEFT, padx=5)
        window.ticker_cb = ttk.Combobox(panel_ctrl, values=window.tickers, state="readonly")
        window.ticker_cb.current(0)
        window.ticker_cb.pack(side=tk.LEFT)

        ttk.Label(panel_ctrl, text="Dzień:").pack(side=tk.LEFT, padx=5)
        window.date_cb = ttk.Combobox(panel_ctrl, values=window.dates, state="readonly")
        window.date_cb.current(0)
        window.date_cb.pack(side=tk.LEFT)

        window.ticker_cb.bind("<<ComboboxSelected>>", lambda e: window.update_plots())
        window.date_cb.bind("<<ComboboxSelected>>", lambda e: window.update_plots())

        window.fig, window.axes = plt.subplots(2, 3, figsize=(12, 8), constrained_layout=True)
        window.canvas = FigureCanvasTkAgg(window.fig, master=window)
        window.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        window.update_plots()

    def update_plots(window):
        ticker = window.ticker_cb.get()
        day = window.date_cb.get()

        sub = window.df[(window.df['Ticker'] == ticker) & (window.df['Data'] == day)]
        sub_all = window.df[window.df['Data'] == day]

        #2for i, ax in enumerate(window.axes.flatten()):
        #2    if i != 3:  
        #2     ax.clear()
    
        window.axes[0, 0].clear()
        window.axes[0, 0].plot(sub['Datetime'], sub['Cena'], marker='o')
        window.axes[0, 0].set_title('Cena akcji')

        window.axes[0, 1].clear()
        window.axes[0, 1].scatter(sub['Return'], sub['Wolumen obrotu'])
        window.axes[0, 1].set_title('Zwrot vs wolumen')

        window.axes[0, 2].clear()
        sub_box = sub.copy()
        sub_box['Hour'] = sub_box['Datetime'].dt.hour
        sub_box.boxplot(column='Return', by='Hour', ax=window.axes[0, 2])
        window.axes[0, 2].set_title('Boxplot zwrot w ujęciu godzinowym')
        window.axes[0, 2].figure.suptitle('')

        window.axes[1, 0].clear()
        #2window.fig.delaxes(window.axes[1, 0])  
        #2window.axes[1, 0] = window.fig.add_subplot(2, 3, 4)  
        pivot = sub_all.pivot_table(index='Datetime_5min', columns='Ticker', values='Return_5min')
        corr = pivot.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        #1if hasattr(window, 'heatmap_colorbar') and window.heatmap_colorbar:   
        #1    window.heatmap_colorbar.remove()                                   
        #1    window.heatmap_colorbar = None
        #1window.axes[1, 0].clear()
        sns.heatmap(corr, mask=mask, cmap="coolwarm", annot=True, fmt=".2f", ax=window.axes[1, 0])
        #1window.heatmap_colorbar = sns_plot.collections[0].colorbar
        window.axes[1, 0].set_title('Heatmap korelacji (5 min)')

        window.axes[1, 1].clear()
        window.axes[1, 1].plot(sub['Datetime'], sub['Spread'], marker='o')
        window.axes[1, 1].set_title('Rozpowszechnianie się w czasie')

        window.axes[1, 2].clear()
        vol_hour = sub.groupby(sub['Hour'])['VolumeDelta'].sum()
        window.axes[1, 2].plot(vol_hour.index, vol_hour.values, marker='o')
        window.axes[1, 2].set_title('Zmiana wolumenu według godziny')

        for ax in window.axes.flatten():
            ax.tick_params(axis='x', rotation=45)

        window.fig.suptitle(f"Analiza: {ticker} - {day}", fontsize=14)
        window.canvas.draw()

    def show_error(window, message):
        err_window = tk.Toplevel(window)
        err_window.title("Błąd")
        err_label = ttk.Label(err_window, text=message, foreground="red")
        err_label.pack(padx=20, pady=20)
        close_btn = ttk.Button(err_window, text="Zamknij", command=window.destroy)
        close_btn.pack(pady=10)

if __name__ == '__main__':
    app = StockApp()
    app.mainloop()
