from scraper.scraper import Scraper
from scraper.config import create_driver
from scraper.utils import save_to_csv
from datetime import datetime, time
import time as systime


def main():
    start_hour = time(9, 0)
    end_hour = time(17, 0)

    while True:
        now = datetime.now()
        current_time = now.time()
        if start_hour <= current_time <= end_hour:
            page_url = (
                "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG20"
            )
            driver = create_driver()
            scraper = Scraper(driver)

            scraper.load_page(page_url)

            data1 = scraper.scrape_wig_20_main_table_data()
            data2 = scraper.scrape_each_wig20_company_data()

            # print_scraped_data(data1)
            # print_scraped_data(data2)

            save_to_csv(data1, "data/data1.csv")
            save_to_csv(data2, "data/data2.csv")

            driver.quit()
            systime.sleep(1800)
        elif current_time < start_hour:
            systime.sleep(300)

        else:
            print("Dzisiejszego dnia sesja jest juz zamknieta")
            break


if __name__ == "__main__":
    main()
