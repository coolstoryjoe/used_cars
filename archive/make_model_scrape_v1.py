
import time
from bs4 import BeautifulSoup as soup

MODELS_MAKES_URL = 'https://www.autotrader.com/cars-for-sale'

# page_soup = soup(pull_url(MODELS_MAKES_URL, 'form-control'), features="lxml")

# makes = page_soup.find('select', {'aria-label': 'Select [object Object]'}).find('optgroup', {'label': 'All Makes'}).find_all('option')

# for make in makes:
#     print(make)
    # make.click()
    # print(page_soup.find('select', {'name': 'ModelCode'}).find('optgroup', {'label': 'All Models'}).find_all('option'))

# make_ex = makes[0]

# print(type(make_ex))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pull_url(url):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    webdriverC = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    with webdriverC as driver:
        driver.implicitly_wait(10)
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'form-control')))
        #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'form-control')))
        
        #el = driver.find_element_by_id('ModelCode2069')
        #eli = driver.find_elements_by_tag_name('optgroup')
        #el = driver.find_element_by_xpath("html/body/div/div/div/div/div/div/div/div/div/form/div/div[@class='col-xs-6 col-sm-4 padding-left-0 padding-left-sm-2']
        el = driver.find_element_by_xpath("//optgroup[contains(@label,'All Makes')]")
        print(el)
        #print(len(eli.text)
        els = el.find_elements_by_tag_name('option')#.getText()
        print(len(els))
        for i in range(len(els)):
            print(els[i].text)
        # for option in el.find_elements_by_tag_name('option'):
        #     print(option.text)
            
        #page_source = driver.page_source
        driver.close()
    return


pull_url(MODELS_MAKES_URL)

# .find('select', {'aria-label': 'Select [object Object]'})
# .find('optgroup', {'label': 'All Makes'})
# .find_all('option')
