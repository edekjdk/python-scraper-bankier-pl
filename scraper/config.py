from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")


def create_driver():
    driver = webdriver.Chrome(options=options)
    return driver
