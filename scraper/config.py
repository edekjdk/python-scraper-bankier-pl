from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver():
    driver = webdriver.Chrome(options=Options())
    return driver
