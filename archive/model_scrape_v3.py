import pandas as pd
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from scraper_v4 import dump_csv_single_col
from scraper_v4 import dump_file
import json

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
cwd = os.getcwd()

BASE_LINK = 'https://www.autotrader.com/cars-for-sale/all-cars?zip=90401&makeCodeList='
NEW_BASE = 'https://www.autotrader.com/cars-for-sale/all-cars/'

def extract_models(link):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(link)
    easy = '/html/body/div[1]/div[1]/div[2]/div/div[2]/a[3]'
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, easy)))

    soups = soup(driver.page_source, features="lxml")
    try:
        sub = soups.find_all('script', {'type': 'text/javascript'})[13].contents[0]
        #print(sub)
        dump_file(sub, 'temp_file.json')
    except:
        pass

    driver.close()
    return

#extract_models(str(NEW_BASE + 'Volkswagen'))

def get_models(MAKE):
    model_code_list = 'modelCodeList|' + MAKE
    file_name = MAKE + '_makes.csv'
    try:
        with open('/Users/josepholeynik/Coding/Python/used_cars/soup_kitchen/temp_file.json') as f:
            version = f.read()
        data = json.loads(version.replace('window.__BONNET_DATA__=', ''))
        makes_list = data['initialState']['domain']['srp']['filters']['options']['modelCodeList'][model_code_list]['options']
        #models_list = data['initialState']['domain']['srp']['filters']['options']['makeCodeList']['options']
        counter = 0
        for i in makes_list:
            dump_csv_single_col(i['value'], file_name, counter)
            counter +=1
    except:
        pass
    with open('/Users/josepholeynik/Coding/Python/used_cars/soup_kitchen/temp_file.json') as f:
        version = f.read()
    data = json.loads(version.replace('window.__BONNET_DATA__=', ''))
    #print(data)
    #makes_list = data['initialState']['domain']['srp']['filters']['options']['modelCodeList']#[model_code_list]['options']
    models_list = data['initialState']['domain']['srp']['filters']['options']['makeCodeList']['options']
    print(models_list[1]['value'])
    #counter = 0
    # for i in makes_list:
    #     #print(i['value'])
    #     dump_csv_single_col(i['value'], file_name, counter)
    #     counter +=1
    return

def pull_save_models(MAKE):
    extract_models(str(NEW_BASE + MAKE))
    get_models(MAKE)
    return

get_models('Volkswagen')

def pull_all_models():
    model_link = str(os.path.join(cwd, 'soup_kitchen', 'makes.csv'))
    df = pd.read_csv(model_link, header=None, names=['Makes'])
    for i in df['Makes']:
        names = i + '_makes.csv'
        if os.path.exists(str(os.path.join(cwd,'soup_kitchen',names))) == False:
            print(i)
            #pull_save_models(i) 
    return

#pull_all_models()
