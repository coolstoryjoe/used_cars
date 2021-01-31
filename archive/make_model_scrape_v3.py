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
    sub_soup = soups.find('optgroup', {'label': 'All Models'})

    print(sub_soup)
    # for SUB in sub_soup:
    #     print(SUB.text)

    #print([o.text for o in select.options])
    
    #print[o.text for o in select.options]  # these are string-s
    #select.select_by_visible_text(....)

#python_button.click()
    
    driver.close()
    return

#pull_url(MODELS_MAKES_URL)


def pull_url1(url):
    chrome_driver_path = '/Users/josepholeynik/Coding/Python/used_cars/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)

    WebDriverWait(driver, 50, ignored_exceptions=ignored_exceptions).until(
        EC.element_to_be_clickable((By.XPATH, "//select[contains(@name,'makeCode')]")))
    driver.find_element_by_xpath(
        "//select[contains(@name,'makeCode')]").click()

    # "//select[contains(@name,'makeCode')]"))
    # select_element = Select(driver.find_element_by_id('makeCode'))
    # select_element.select_by_value('MIT')

    soups = soup(driver.page_source, features="lxml")
    sub_soup = soups.find('optgroup', {'label': 'All Models'})

    print(sub_soup)

    # with webdriverC as driver:

        #
    #WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'form-control')))
        #iframe = driver.find_element_by_tag_name("iframe")

        #driver.switch_to.frame(iframe)
        #wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//li[.="Bass"]'))).click()
        # links = wait(driver, 10).until(EC.presence_of_all_elements_located(
        #     (By.XPATH, '//section[@id="search-results"]//a[.//*[name()="svg"]]')))

        # for link in links:
        #     print(link.get_attribute('href'))

 
        # soups = soup(driver.page_source, features="lxml")
        # sub_soup = soups.find('optgroup',{'label':'All Makes'})
        
        # for su_vid in sub_soup:
        #     print(su_vid.text)

        # subx = sub_soup.find('option')

        

        # print(subx)        
        # selection = driver.find_element_by_xpath("// optgroup[contains(@label, 'All Makes')]")
        #select.select_by_visible_text('AMC')

        # soups2 = soup(driver.page_source, features="lxml")
        
        # sub_soup2 = soups2.find('optgroup', {'label': 'All Models'})
        # print(sub_soup2)

        # for su2 in sub_soup2:
        #     print(su2.text)

        #els = el.find_elements_by_tag_name('option')#.getText()
        
        #print(len(els))

        # for i in range(len(els)):
        #     print(els[i].text)

        
            
        #page_source = driver.page_source

# .find('select', {'aria-label': 'Select [object Object]'})
# .find('optgroup', {'label': 'All Makes'})
# .find_all('option')

# page_soup = soup(pull_url(MODELS_MAKES_URL, 'form-control'), features="lxml")

# makes = page_soup.find('select', {'aria-label': 'Select [object Object]'}).find('optgroup', {'label': 'All Makes'}).find_all('option')

# for make in makes:
#     print(make)
# make.click()
# print(page_soup.find('select', {'name': 'ModelCode'}).find('optgroup', {'label': 'All Models'}).find_all('option'))

# make_ex = makes[0]

# print(type(make_ex))
