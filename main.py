from scraper.scraper import Scraper
from scraper.config import create_driver


def main():
    page_url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG20"
    driver = create_driver()
    scraper = Scraper(driver)

    scraper.load_page(page_url)
    scraper.scrape_data()

    driver.quit()


if __name__ == "__main__":
    main()
