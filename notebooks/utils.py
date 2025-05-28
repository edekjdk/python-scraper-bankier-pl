import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re


def draw_plot(ticker, table):
    to_show = table.loc[table.Ticker == ticker]
    to_show = to_show.loc[:, ["Nazwa", "Cena", "Godzina", "Data"]]
    to_show["Godzina"] = pd.to_datetime(to_show["Godzina"], format="%H:%M:%S")

    plt.figure(figsize=(10, 5))
    ax = to_show.plot(x="Godzina", y="Cena", marker="o")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    title_string = to_show["Nazwa"].iloc[0]
    subtitle_string = to_show["Data"].iloc[0]

    plt.xticks(rotation=45)
    plt.suptitle(title_string, y=1.00, fontsize=14)
    plt.title(subtitle_string, fontsize=10)
    ax.set_ylabel("Cena [PLN]")
    plt.tight_layout()
    plt.show()



def parse_number(text):
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)

    cleaned = (
        str(text)
        .replace(",", ".")
        .replace(" ", "")
        .replace("zł", "")
        .replace("%", "")
        .replace("szt", "")
        .replace("mln", "")
    )
    cleaned = re.sub(r"\(.*?\)", "", cleaned) 

    try:
        return float(cleaned)
    except ValueError:
        return text
