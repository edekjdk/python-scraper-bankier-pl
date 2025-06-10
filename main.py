from scraper.scraper import Scraper
from scraper.config import create_driver
from scraper.utils import save_to_csv
from datetime import datetime
import sys


def main():
    page_url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG20"
    hour = datetime.now().hour

    if 8 <= hour <= 20:
        driver = create_driver()
        scraper = Scraper(driver)

        scraper.load_page(page_url)

        data1 = scraper.scrape_wig_20_main_table_data()
        data2 = scraper.scrape_each_wig20_company_data()

        save_to_csv(data1, "data/data1.csv")
        save_to_csv(data2, "data/data2.csv")

        driver.quit()


if __name__ == "__main__":
    if "--gui" in sys.argv:
        from gui import GuiApp

        app = GuiApp()
        app.mainloop()
    else:
        main()
