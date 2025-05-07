from scraper.scraper import Scraper
from scraper.config import create_driver


def main():
    page_url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG20"
    driver = create_driver()
    scraper = Scraper(driver)

    scraper.load_page(page_url)

    # scraper.scrape_wig_20_main_table_data()
    scraper.scrape_each_wig20_company_data()

    driver.quit()


if __name__ == "__main__":
    main()
