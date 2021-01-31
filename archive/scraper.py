from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def parse(url):
    uClient = uReq(url)
    url_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    return(url_soup)

def pull_url(url):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'    
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    webdriverC = webdriver.Chrome(executable_path = chrome_driver_path, options = chrome_options)
    #webdriverC = webdriver.Chrome(ChromeDriverManager().install())#, options = chrome_options)
    with webdriverC as driver:
        #wait = WebDriverWait(driver, 20)#.until(EC.presence_of_element_located((By.CLASS_NAME, "first-price")))
        #element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'first-price')))
        wait = WebDriverWait(driver, 30)
        driver.implicitly_wait(10)
        driver.get(url)    
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'first-price')))
        #results = driver.find_element_by_class_name('first-price').text
        quotesoup = soup(driver.page_source, features="lxml")
        driver.close()
    
    #redsoup = (quotesoup.find('span',{'class':'first-price'}).text)
    return(quotesoup)

# AutoTrader.com
AUTOTRADE = 'https://www.autotrader.com/cars-for-sale/all-cars?zip=90401&makeCodeList=TOYOTA&modelCodeList=TACOMA'
print(pull_url(AUTOTRADE))

# CarsDirect.com
# Hemmings.com
# Autolist.com
# CarGurus.com
# AutoTempest.com
# KBB.com (Kelley Blue Book)
# Cars & Bids
