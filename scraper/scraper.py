from selenium.webdriver.common.by import By
from datetime import date
from datetime import datetime


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, page_url):
        self.driver.get(page_url)

    def scrape_wig_20_main_table_data(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "table.sortTableMixedData")
        table_head = table.find_element(By.TAG_NAME, "thead")
        table_body = table.find_element(By.TAG_NAME, "tbody")
        table_head_ths = table_head.find_elements(By.TAG_NAME, "th")
        table_head_items = []

        table_body_rows = table_body.find_elements(By.TAG_NAME, "tr")
        table_data = []

        for th in table_head_ths:
            th = th.get_attribute("innerHTML")[38:-6]  # refactor
            th = th.replace("<br>", " ")
            table_head_items.append(th)

        for row in table_body_rows[1:]:
            tds = row.find_elements(By.TAG_NAME, "td")
            row_values = [td.text for td in tds]
            row_dict = {key: value for key, value in zip(table_head_items, row_values)}
            table_data.append(row_dict)
        return table_data

    def scrape_each_wig20_company_data(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "table.sortTableMixedData")
        table_body = table.find_element(By.TAG_NAME, "tbody")

        table_links = table_body.find_elements(By.TAG_NAME, "a")
        links_to_visit = [link.get_attribute("href") for link in table_links]
        all_data = []

        for link in links_to_visit:
            self.driver.get(link)
            ticker = link.split("symbol=")[-1]

            company_name = self.driver.find_element(
                By.CSS_SELECTOR, "a.profilHead"
            ).text
            company_main_price = self.driver.find_element(
                By.CSS_SELECTOR, "div.profilLast"
            ).text

            company_table = self.driver.find_element(
                By.CSS_SELECTOR, "table.summaryTable"
            )
            company_table_body = company_table.find_element(By.TAG_NAME, "tbody")
            company_table_tds = company_table_body.find_elements(By.TAG_NAME, "td")
            keys = []
            values = []
            for td in company_table_tds:
                if len(td.text) > 0:
                    if ":" in td.text:
                        keys.append(td.text[:-1])
                    else:
                        values.append(self._parse_number(td.text))
            row_dict = {
                "Ticker": ticker,
                "Nazwa": company_name,
                "Cena": self._parse_number(company_main_price),
                "Data": date.today().strftime("%Y-%m-%d"),
                "Godzina": datetime.now().strftime(("%H:%M:%S")),
                **{key: value for key, value in zip(keys, values)},
            }
            all_data.append(row_dict)

        return all_data

    def _parse_number(self, text):
        if text is None:
            return None
        text = (
            text.replace(" ", "").replace("zł", "").replace("%", "").replace(",", ".").replace("mln", "").replace("tys", "").replace("mld", "").replace("szt", "")
        )
        try:
            return float(text)
        except ValueError:
            return text