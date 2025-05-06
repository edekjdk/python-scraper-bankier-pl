from scraper.scraper import Scraper
from scraper.config import create_driver
import time


def main():
    page_url = "https://bankier.pl"
    driver = create_driver()
    scraper = Scraper(driver)

    scraper.load_page(page_url)
    scraper.scrape_data()

    time.sleep(2)

    driver.quit()


if __name__ == "__main__":
    main()
