from scraper.scraper import Scraper
from scraper.config import create_driver
from scraper.utils import save_to_csv


def main():
    page_url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG20"
    driver = create_driver()
    scraper = Scraper(driver)

    scraper.load_page(page_url)

    data1 = scraper.scrape_wig_20_main_table_data()
    # data2 = scraper.scrape_each_wig20_company_data()

    # print_scraped_data(data1)
    # print_scraped_data(data2)

    save_to_csv(data1, "Dane1.csv")
    # save_to_csv(data2, "Dane2.csv")

    driver.quit()


if __name__ == "__main__":
    main()
