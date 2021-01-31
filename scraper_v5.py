import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from models import save_obj, load_obj, dump_csv_single_col, dump_csv, dump_file
from collections import defaultdict

AUTOTRADE = 'https://www.autotrader.com/cars-for-sale/all-cars/toyota/tacoma/santa-monica-ca-90401?dma=&searchRadius=0&location=&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord='

cwd = os.getcwd()

# Pull page with Selenium waiting for a class name to be located
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

#iterate through Autotrader make and model page to pull and parse html to extract pricing and other features
def pull_AutoTrader(BASE_LINK):
    dicts = defaultdict(list)
    counter = 0
    for i in range(0,1300,100):
        new_url = BASE_LINK + str(i)
        #print(new_url)
        page_soup = soup(pull_url(new_url, 'first-price'), features="lxml")
        sub_soup = page_soup.find('div',{'data-qaid':'cntnr-listings'})
        inventory = sub_soup.find_all('div',{'data-cmp':'inventoryListing'})
        for j in inventory:
            try:
                Name = j.find('h2',{'data-cmp':'subheading'}).text
                X = Name.split()

                STATUS = X[0]
                YEAR = X[1]
                MAKE = X[2]
                MODEL = X[3]
                PRICE = j.find('span', {'class': 'first-price'}).text
                
                otherstuff = j.find('ul', {'class': 'list list-inline display-inline margin-bottom-0'}).find_all('li')

                if len(otherstuff) == 4:
                    for k in otherstuff:
                        text = k.find('span', {'class': 'text-gray-base text-size-200 text-size-sm-300'}).text
                        x = text.split(':')
                        dicts[x[0]] = (x[1])
                else: 
                    nope = 'n/a'
                    dicts['Color'] = nope 
                    dicts['MPG'] = nope
                    dicts['Drive Type']= nope 
                    dicts['Engine'] = nope

                COLOR = dicts['Color']
                MPG = dicts['MPG']
                DRIVE = dicts['Drive Type']
                ENGINE = dicts['Engine']

                items = [STATUS, YEAR, MAKE, MODEL, PRICE, COLOR , MPG , DRIVE, ENGINE]

                dump_csv(items,'AutoTrade.csv',counter)
                #print('dump #', counter)
                counter +=1
            except:
                pass
    return

# create query urls to iterate through using the pull_AutoTrader() func based on a make and model
def create_url(make,model):
    BASE = 'https://www.autotrader.com/cars-for-sale/all-cars/'
    SECOND = '/'
    THIRD = '/santa-monica-ca-90401?dma=&searchRadius=0&location=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord='
    URL = str(BASE + make + SECOND + model + THIRD)
    #print(URL)
    return URL

# open a auto_trade make and model information file as saved down by pull_AutoTrader() func
def open_seseme():
    HEADERS = ['status', 'year', 'make', 'model',
               'Price', 'COLOR', 'MPG', 'DRIVE', 'ENGINE']
    df = pd.read_csv(
        str(os.path.join(cwd, 'soup_kitchen', 'AutoTrade.csv')), names=HEADERS)
    df['age'] = 2021 - df['year']
    df = df.sort_values(by=['age'])
    return df

# create DataFrame of used car options based on make and model 
def make_model_query(make,model):
    try:
        pull_AutoTrader(create_url(make, model))
    except:
        pass
    df1 = open_seseme()
    df1 = df1[df1.status == 'Used'].reset_index().drop(['index'], axis = 1)
    df1['Price'] = df1['Price'].str.replace(',', '').astype('int32')
    return(df1)
