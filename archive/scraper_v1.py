from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

AUTOTRADE = 'https://www.autotrader.com/cars-for-sale/all-cars/toyota/tacoma/santa-monica-ca-90401?dma=&searchRadius=0&location=&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord='

cwd = os.getcwd()

def parse(url):
    uClient = uReq(url)
    url_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    return(url_soup)

def pull_url(url,class_name):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'    
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    webdriverC = webdriver.Chrome(executable_path = chrome_driver_path, options = chrome_options)
    with webdriverC as driver:
        wait = WebDriverWait(driver, 30)
        driver.implicitly_wait(10)
        driver.get(url)    
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,class_name)))
        page_source = driver.page_source
        driver.close()
    return(page_source)

def dump_file(obj,file_name): 
    with open(str(os.path.join(cwd,'soup_kitchen',file_name)),'w') as f:
        f.write(obj)
    return

def dump_csv(myCsvRow, file_name ,row_index):        
    if row_index == 0:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(myCsvRow)
    else:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(myCsvRow)
    return

# AutoTrader.com
def pull_AutoTrader():
    for i in range(0,1300,100):
        new_url = AUTOTRADE + str(i)
        page_soup = soup(pull_url(new_url, 'first-price'), features="lxml")
        sub_soup = page_soup.find('div',{'data-qaid':'cntnr-listings'})
        inventory = sub_soup.find_all('div',{'data-cmp':'inventoryListing'})
        for i in inventory:
            try:
                print('writing line')
                Name = i.find('h2',{'data-cmp':'subheading'}).text
                Price = i.find('span',{'class':'first-price'}).text
                items = [Name, Price]
                dump_csv(items,'AutoTrade.csv',i)
            except:
                pass

pull_AutoTrader()
#dump_file(pull_url(AUTOTRADE,'first-price'),'AutoTrader_p2.html')

# with open(str(os.path.join(cwd,'soup_kitchen','AutoTrader_p2.html')),'r') as f:
#     page_soup = soup(f,features="lxml")

# sub_soup = page_soup.find('div',{'data-qaid':'cntnr-listings'})
# inventory = (sub_soup.find_all('div',{'data-cmp':'inventoryListing'}))

# for i in inventory:
#     print(i.find('h2',{'data-cmp':'subheading'}).text ,": " ,i.find('span',{'class':'first-price'}).text)
