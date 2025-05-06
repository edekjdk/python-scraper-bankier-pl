from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, page_url):
        self.driver.get(page_url)

    def scrape_data(self):
        table_xpath = "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div[6]/div[2]/table[1]"
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_rows = table.find_elements(By.TAG_NAME, "tr")
        for i, row in enumerate(table_rows[1:]):
            print(i + 1, end=" ")
            tds = row.find_elements(By.TAG_NAME, "td")
            for td in tds[1:]:
                td_text = td.get_attribute("innerHTML")
                if "&nbsp;" in td_text:
                    td_text = td_text.replace("&nbsp;", " ")
                print(td_text, end="      ")
            print()
