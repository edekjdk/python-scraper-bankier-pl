import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


class GuiApp(tk.Tk):
    def __init__(self, data_path="data/data2.csv"):
        super().__init__()

        self.title("Wykresy spółek WIG20")
        self.geometry("1920x1080")

        # Podmiana domyślnego zachowania pod zamykaniem okna
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Sprawdzanie czy są dane
        if not os.path.exists(data_path):
            self.show_error("Plik danych nie istnieje. Najpierw zescrapuj dane.")
            return

        # Wywołania metod
        self.load_data(data_path)
        self.create_controls()
        self.create_plots()
        self.update_plots()

    def on_closing(self):
        plt.close("all")  # Zamknięcie wykresów
        self.destroy()  # Zamknięcie okna
        self.quit()  # Zamknięcie aplikacji

    def load_data(self, data_path):
        self.df = pd.read_csv(data_path)

    
        # Przygotowanie danych
        self.df["Datetime"] = pd.to_datetime(self.df["Data"] + " " + self.df["Godzina"])
        self.df.sort_values(["Ticker", "Datetime"], inplace=True)
        self.df["Return"] = self.df.groupby("Ticker")["Cena"].pct_change() * 100
        self.df["Hour"] = self.df["Datetime"].dt.hour
        self.df["Spread"] = self.df["Max 1D"] - self.df["Min 1D"]
        self.df["VolumeDelta"] = self.df.groupby(["Ticker", "Data"])["Wartość obrotu"].diff()
        self.df["Datetime_5min"] = self.df["Datetime"].dt.floor("5min")
        self.df["Return_5min"] = self.df.groupby("Ticker")["Cena"].pct_change() * 100
        self.tickers = sorted(self.df["Ticker"].unique())
        self.dates = sorted(self.df["Data"].unique())

    def create_controls(self):
        # Ramka na przyciski
        control_panel = ttk.Frame(self)
        control_panel.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Etykieta wyboru spółki (dropdown)
        ttk.Label(control_panel, text="Spółka:").pack(side=tk.LEFT, padx=5)
        self.ticker_combo = ttk.Combobox(
            control_panel, values=self.tickers, state="readonly"
        )
        self.ticker_combo.current(0)
        self.ticker_combo.pack(side=tk.LEFT)

        # Etykieta wyboru daty (dropdown)
        ttk.Label(control_panel, text="Dzień:").pack(side=tk.LEFT, padx=5)
        self.date_combo = ttk.Combobox(
            control_panel, values=self.dates, state="readonly"
        )
        self.date_combo.current(0)
        self.date_combo.pack(side=tk.LEFT)

        # Powiązanie zmiany wyboru w dropdownie z aktualizacją wykresów
        self.ticker_combo.bind("<<ComboboxSelected>>", lambda e: self.update_plots())
        self.date_combo.bind("<<ComboboxSelected>>", lambda e: self.update_plots())

    def create_plots(self):
        # Utworzenie figury matplotlib
        self.fig, self.axes = plt.subplots(2, 3, figsize=(12, 8))
        self.fig.tight_layout(pad=3.0)

        # Utworzenie tła tkinter do wyświetlenia figury matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_plots(self):  # Główna funkcja aktualizująca
        # Pobranie wybranej spółki i dnia z list rozwijanych
        ticker = self.ticker_combo.get()
        day = self.date_combo.get()

        # Filtrowanie danych
        stock_data = self.df[(self.df["Ticker"] == ticker) & (self.df["Data"] == day)]
        all_stocks_day = self.df[self.df["Data"] == day]

        # Wyczyszczenie istniejących wykresów
        self.fig.clear()
        self.axes = self.fig.subplots(2, 3)  # Ponowne utworzenie siatki

        # Generowanie wykresów
        self.plot_stock_price(stock_data)
        self.plot_return_vs_volume(stock_data)
        self.plot_hourly_returns(stock_data)
        self.plot_correlation_heatmap(all_stocks_day)
        self.plot_spread(stock_data)
        self.plot_volume_change(stock_data)

        # Główny tytuł
        self.fig.suptitle(f"{ticker} - {day}", fontsize=14, y=0.98)
        self.fig.tight_layout(
            rect=[0, 0.03, 1, 0.95]
        )  # Dostosowanie układu, by pomieścić tytuł
        self.canvas.draw()  # Odświeżenie wyświetlanych wykresów

    def plot_stock_price(self, data):  # Wykres ceny akcji
        ax = self.axes[0, 0]

        if not data.empty:
            ax.plot(
                data["Datetime"], data["Cena"], marker="o", markersize=4, linewidth=1.5
            )
            if len(data) > 3:  # Linia trendu jeśli jest więcej danych niż 3 odczyty
                x_numeric = np.arange(len(data))
                trend = np.polyfit(x_numeric, data["Cena"], 1)
                trend_line = np.poly1d(trend)
                ax.plot(
                    data["Datetime"],
                    trend_line(x_numeric),
                    color="red",
                    linestyle="--",
                    alpha=0.7,
                    label="Trend",
                )
                ax.legend(fontsize=8)  # Legenda z linia trendu

        ax.set_title("Cena akcji")
        ax.set_ylabel("Cena (PLN)")
        ax.tick_params(axis="x", rotation=45)  # Obrócone etykiety na osi X

    def plot_return_vs_volume(self, data):  # Zwrot vs Wolumen
        ax = self.axes[0, 1]

        if not data.empty and not data["Return"].isna().all():
            clean_data = data.dropna(subset=["Return", "Wolumen obrotu"])
            if not clean_data.empty:
                ax.scatter(
                    clean_data["Return"], clean_data["Wolumen obrotu"], alpha=0.6, s=30
                )
                ax.axvline(
                    x=0, color="red", linestyle="--", alpha=0.7, label="0% zwrot"
                )  # Punkt odniesienia 0%
                ax.axhline(
                    y=clean_data["Wolumen obrotu"].median(),
                    color="orange",
                    linestyle="--",
                    alpha=0.5,
                    label="Mediana wolumenu",
                )  # Mediana
                ax.legend(fontsize=8)  # Legenda

        ax.set_title("Zwrot vs wolumen")
        ax.set_xlabel("Zwrot (%)")
        ax.set_ylabel("Wolumen")

    def plot_hourly_returns(self, data):  # Zwrot według godziny
        ax = self.axes[0, 2]

        if not data.empty and not data["Return"].isna().all():
            hourly_avg = data.groupby("Hour")["Return"].mean()
            if not hourly_avg.empty:
                ax.plot(
                    hourly_avg.index,
                    hourly_avg.values,
                    marker="o",
                    markersize=6,
                    linewidth=2,
                )  # Punkt odniesienia 0%
                ax.axhline(y=0, color="red", linestyle="--", alpha=0.5)

        ax.set_title("Zwrot według godzin")
        ax.set_xlabel("Godzina")
        ax.set_ylabel("Zwrot (%)")

    def plot_correlation_heatmap(self, data):  # Macierz korelacji
        ax = self.axes[1, 0]
        if not data.empty:
            pivot = data.pivot_table(
                index="Datetime_5min", columns="Ticker", values="Return_5min"
            )

            # Obliczenia
            corr_matrix = pivot.corr()

            if not corr_matrix.empty and len(corr_matrix) > 1:
                # Usuniecie zbędnych danych
                mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

                masked_corr = corr_matrix.copy()
                masked_corr[mask] = np.nan

                # Heatmapa z paletą kolorów
                im = ax.imshow(
                    masked_corr, cmap="RdBu_r", aspect="auto", vmin=-1, vmax=1
                )

                # Osie
                tickers = corr_matrix.columns
                ax.set_xticks(range(len(tickers)))
                ax.set_yticks(range(len(tickers)))
                ax.set_xticklabels(tickers, rotation=45, ha="right")
                ax.set_yticklabels(tickers)

                # Wpisane wartości w macierz
                # for i in range(len(tickers)):
                #     for j in range(len(tickers)):
                #         if i > j:
                #             value = corr_matrix.iloc[i, j]
                #             if not np.isnan(value):
                #                 ax.text(
                #                     j,
                #                     i,
                #                     f"{value:.2f}",
                #                     ha="center",
                #                     va="center",
                #                     color="black",
                #                     fontweight="normal",
                #                 )

                # Legenda kolorów
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label("Korelacja", rotation=270, labelpad=15)

        ax.set_title("Korelacja zwrotów między spółkami")

    def plot_spread(self, data):  # Spread w czasie
        ax = self.axes[1, 1]

        if not data.empty and not data["Spread"].isna().all():
            clean_data = data.dropna(subset=["Spread"])
            if not clean_data.empty:
                ax.plot(
                    clean_data["Datetime"],
                    clean_data["Spread"],
                    marker="o",
                    markersize=4,
                    linewidth=1.5,
                )
                avg_spread = clean_data["Spread"].mean()  # Średni spread
                ax.axhline(
                    y=avg_spread,
                    color="green",
                    linestyle="--",
                    alpha=0.7,
                    label=f"Średni spread: {avg_spread:.2f}",
                )
                ax.legend(fontsize=8)  # Legenda

        ax.set_title("Spread w czasie")
        ax.set_xlabel("Czas")
        ax.set_ylabel("Spread (PLN)")
        ax.tick_params(axis="x", rotation=45)

    def plot_volume_change(self, data):  # Wolumen wg godziny
        ax = self.axes[1, 2]
        
        if not data.empty and not data["VolumeDelta"].isna().all():
            hourly_volume = data.groupby("Hour")["VolumeDelta"].sum()
            if not hourly_volume.empty:
                ax.bar(
                    hourly_volume.index,
                    hourly_volume.values,
                    color="green",
                    alpha=0.7,
                    width=0.6,
                )
                ax.axhline(
                    y=0, color="black", linestyle="-", alpha=0.8
                )  # Punkt odniesienia 0

        ax.set_title("Wolumen według godziny")
        ax.set_xlabel("Godzina")
        ax.set_ylabel("Wolumen")
        ax.grid(True, alpha=0.3)

    def show_error(self, message):  # Wyświetlanie błędów
        error_window = tk.Toplevel(self)
        error_window.title("Błąd")
        error_window.geometry("300x150")

        label = ttk.Label(error_window, text=message, foreground="red")
        label.pack(padx=20, pady=20)

        button = ttk.Button(error_window, text="Zamknij", command=error_window.destroy)
        button.pack(pady=10)


if __name__ == "__main__":
    app = GuiApp()
    app.mainloop()
