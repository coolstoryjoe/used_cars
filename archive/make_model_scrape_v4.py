import time
from bs4 import BeautifulSoup as soup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from scraper_v4 import dump_csv_single_col

MODELS_MAKES_URL = 'https://www.autotrader.com/cars-for-sale'

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

def pull_url(url):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)
    
    WebDriverWait(driver, 50, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name,'makeCode')]")))
    driver.find_element_by_xpath("//select[contains(@name,'makeCode')]").click()

    # "//select[contains(@name,'makeCode')]"))
    # select_element = Select(driver.find_element_by_id('makeCode'))
    # select_element.select_by_value('MIT')

    soups = soup(driver.page_source, features="lxml")
    sub_soup = soups.find('optgroup', {'label': 'All Makes'})
    counter = 0
    for sub in sub_soup.find_all('option'):
        val = sub.text#['value']
        print(val)
        dump_csv_single_col(val, 'makes.csv', counter)
        counter +=1
        #print(sub['value'])  
    # print(sub_soup)
    driver.close()
    return

#pull_url(MODELS_MAKES_URL)
