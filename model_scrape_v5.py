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
from scraper_v5 import make_model_query
import json
from models import save_obj, load_obj, dump_csv_single_col, dump_csv, dump_file
import time 

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
cwd = os.getcwd()

BASE_LINK = 'https://www.autotrader.com/cars-for-sale/all-cars?zip=90401&makeCodeList='
NEW_BASE = 'https://www.autotrader.com/cars-for-sale/all-cars/'

#pull all the makes for a given model - returns a list
def extract_models(MAKE):
    return_list = []
    link = str(NEW_BASE + MAKE)
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
        data = json.loads(sub.replace('window.__BONNET_DATA__=', ''))
        
        makes_list = data['initialState']['domain']['srp']['filters']['options']['makeCodeList']['options']
        d = {i['label']: i['value'] for i in makes_list}
        make = d[MAKE]

        model_code_list = 'modelCodeList|' + make
        #file_name = make + '_makes.csv'

        models_list = data['initialState']['domain']['srp']['filters']['options']['modelCodeList'][model_code_list]['options']

        #counter = 0
        for i in models_list:
                return_list.append(i['label'])
    except:
        pass
    driver.close()
    return return_list

#pull a dict of all makes and thier key name in Autotrader website
def extract_makes():
    link = str(NEW_BASE + 'Volkswagen')
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(link)

    easy = '/html/body/div[1]/div[1]/div[2]/div/div[2]/a[3]'

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, easy)))

    soups = soup(driver.page_source, features="lxml")

    try:
        sub = soups.find_all(
            'script', {'type': 'text/javascript'})[13].contents[0]
        data = json.loads(sub.replace('window.__BONNET_DATA__=', ''))

        makes_list = data['initialState']['domain']['srp']['filters']['options']['makeCodeList']['options']
        d = {i['label']: i['value'] for i in makes_list}
    except:
        pass
    return d

# pull all of the makes for all of the models and save down as Master_Keys.pkl
def pull_all_makes_and_models():
    temp_dict = {}
    makes = extract_makes()
    for i in makes.keys():
        temp_dict[i] = extract_models(i)

        if len(temp_dict[i]) == 0:
            temp_dict[i] = extract_models(i)
        if len(temp_dict[i]) == 0:
            temp_dict[i] = extract_models(i)

    save_obj(temp_dict, 'Master_Keys')
    return

# create dataframe of pricing from all makes and models in Autotrader Site
def pull_master_price_list():
    make_model_dict = load_obj('Master_Keys')
    df = pd.DataFrame()
    for k , v in make_model_dict.items():
        if k == 'Toyota':
            for i in v:
                if i == '4Runner' or i == 'Tacoma':
                    print(k,i)
            #     time.sleep(10)
                    df = df.append(make_model_query(k, i))
    save_obj(df,'Toyota_Exaple_DF')
    return 

#pull_all_makes_and_models()

pull_master_price_list()
