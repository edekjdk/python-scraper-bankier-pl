from selenium.webdriver.common.by import By
from datetime import date


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, page_url):
        self.driver.get(page_url)

    def scrape_wig_20_main_table_data(self):
        table_head_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]/thead"
        table_head = self.driver.find_element(By.XPATH, table_head_xpath)
        table_head_ths = table_head.find_elements(By.TAG_NAME, "th")
        table_head_items = []

        table_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]"
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_rows = table.find_elements(By.TAG_NAME, "tr")
        table_data = []

        for th in table_head_ths:
            th = th.get_attribute("innerHTML")[38:-6]  # refactor
            th = th.replace("<br>", " ")
            table_head_items.append(th)

        for row in table_rows[1:]:
            tds = row.find_elements(By.TAG_NAME, "td")
            row_values = [td.text for td in tds]
            row_dict = {key: value for key, value in zip(table_head_items, row_values)}
            table_data.append(row_dict)

        return table_data
        # for i in table_data:
        #     print("------")
        #     for k, v in i.items():
        #         print("{}: {}".format(k, v))

    def scrape_each_wig20_company_data(self):
        table_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]"
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_links = table.find_elements(By.TAG_NAME, "a")
        links_to_visit = [link.get_attribute("href") for link in table_links]
        all_data = []
        for link in links_to_visit:
            self.driver.get(link)
            company_name_xpath = (
                "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[1]/span/a"
            )
            comapany_table_xpath = "/html/body/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/table/tbody"
            company_main_price_xpath = (
                "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]"
            )

            company_table = self.driver.find_element(By.XPATH, comapany_table_xpath)
            company_table_tds = company_table.find_elements(By.TAG_NAME, "td")
            company_name = self.driver.find_element(By.XPATH, company_name_xpath).text
            company_main_price = self.driver.find_element(
                By.XPATH, company_main_price_xpath
            ).text
            keys = []
            values = []
            for td in company_table_tds:
                if len(td.text) > 0:
                    if ":" in td.text:
                        keys.append(td.text[:-1])
                    else:
                        values.append(td.text)
            row_dict = {
                "Nazwa": company_name,
                "Cena": company_main_price,
                "Data": date.today().strftime("%Y-%m-%d"),
                **{key: value for key, value in zip(keys, values)},
            }
            all_data.append(row_dict)

            return all_data
            # for i in all_data:
            #     print("------")
            #     for k, v in i.items():
            #         print("{}: {}".format(k, v))
