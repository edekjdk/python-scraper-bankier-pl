from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, page_url):
        self.driver.get(page_url)

    def scrape_wig_20_main_table_data(self):
        table_head_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]/thead"
        table_head = self.driver.find_element(By.XPATH, table_head_xpath)
        table_head_items = []
        table_head_ths = table_head.find_elements(By.TAG_NAME, "th")

        table_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]"
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_rows = table.find_elements(By.TAG_NAME, "tr")
        table_data = []

        for th in table_head_ths:
            th = th.get_attribute("innerHTML")[38:-6]  # refactor
            th = th.replace("<br>", " ")
            table_head_items.append(th)

        for row in table_rows[1:]:
            row_values = []
            tds = row.find_elements(By.TAG_NAME, "td")
            for td in tds:
                td_text = td.get_attribute("innerHTML")
                if "&nbsp;" in td_text:
                    td_text = td_text.replace("&nbsp;", " ")
                if "<a" in td_text:
                    td_text = td_text[td_text.index(">") + 1 : -4]  # refactor
                row_values.append(td_text)
            row_dict = {key: value for key, value in zip(table_head_items, row_values)}
            table_data.append(row_dict)

        for i in table_data:
            print("------")
            for k, v in i.items():
                print("{}: {}".format(k, v))
