import numpy as np
from sklearn.svm import SVR
import warnings
warnings.filterwarnings("ignore")
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
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
import seaborn as sns
import matplotlib.pyplot as plt

AUTOTRADE = 'https://www.autotrader.com/cars-for-sale/all-cars/toyota/tacoma/santa-monica-ca-90401?dma=&searchRadius=0&location=&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord='
from collections import defaultdict
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

def pull_AutoTrader():
    dicts = defaultdict(list)
    for i in range(0,1300,100):
        new_url = AUTOTRADE + str(i)
        page_soup = soup(pull_url(new_url, 'first-price'), features="lxml")
        sub_soup = page_soup.find('div',{'data-qaid':'cntnr-listings'})
        inventory = sub_soup.find_all('div',{'data-cmp':'inventoryListing'})
        for j in inventory:
            try:
                Name = j.find('h2',{'data-cmp':'subheading'}).text
                X = Name.split()
                status = X[0]
                year = X[1]
                make = X[2]
                model = X[3]
                Price = j.find('span',{'class':'first-price'}).text
                
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

                items = [status, year, make, model, Price, COLOR , MPG , DRIVE, ENGINE]

                dump_csv(items,'AutoTrade.csv',i)
            except:
                pass
    #print(dicts.keys())
    return

def plot_graph(age, price):
    X = age.values[:, np.newaxis]
    y = price.values

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 50000)

    clf = SVR(kernel='rbf', C=5000,  epsilon=0.5)
    clf.fit(X, df.Price)

    plt.plot(X, clf.predict(X), color='k')
    plt.plot(age, price, 'o')
    plt.show()
    return

#pull_AutoTrader()

HEADERS = ['status', 'year', 'make', 'model', 'Price', 'COLOR' , 'MPG' , 'DRIVE', 'ENGINE']
df = pd.read_csv(str(os.path.join(cwd, 'soup_kitchen', 'AutoTrade.csv')),names=HEADERS)
df['age'] = 2021 - df['year']
df = df.sort_values(by = ['age'])

pd.set_option('display.max_columns', None)

listicle = df.ENGINE.unique()

df_6 = df[df.ENGINE == ' 6-Cylinder']
df_4 = df[df.ENGINE == ' 4-Cylinder']

df = df[df.status == 'Used'].reset_index().drop(['status', 'make', 'model', 'index','year'], axis=1)
df['Price'] = df['Price'].str.replace(',', '').astype('int32')
plot_graph(df.age,df.Price)
