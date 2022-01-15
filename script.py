from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import yaml
import csv

from css_selectors import next_button_selector, listings_selector, listing_name_selector, listing_rating_selector, result_file_name 


#Driver setup

# try:
#     with open("conf.yaml", 'r') as stream:
#         chrome_driver = yaml.safe_load(stream).get('chrome_driver')
# except:
    # print('Unable to read driver location')
chrome_driver = os.environ.get('CHROME_DRIVER')
driver=webdriver.Chrome(executable_path=chrome_driver)

#Result object
result = {}
headerrow = ['Name and Description', 'Rating']

#Starting the driver
driver.get('https://www.airbnb.com/s/Boston--MA--United-States/homes?place_id=ChIJGzE9DS1l44kRoOhiASS_fHg&refinement_paths%5B%5D=%2Fhomes&adults=0&children=0&infants=0&pets=0&search_type=AUTOSUGGEST')

#Allow loading time for the whole page to render. Since Airbnb is a SPA, a lot of backend calls are involved
time.sleep(7)

def each_page():
    while True:
        #Scrolling to the bottom of the page, for the next button to render
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);")
        time.sleep(1)
        
        #Selecting a list of all listings on this page
        listings = driver.find_elements(By.CSS_SELECTOR,listings_selector)
        
        for list in listings:
            name_of_listing = list.find_element(By.CSS_SELECTOR,listing_name_selector).text
            if name_of_listing in result:
                continue
            try:
                rating_of_listing = list.find_element(By.CSS_SELECTOR,listing_rating_selector).text
            except:
                #Listing does not have a rating
                rating_of_listing = 'No Rating'
            result[name_of_listing] = [name_of_listing, rating_of_listing]
        
        #Handling pagination of results    
        next_page_button = driver.find_element(By.CSS_SELECTOR,next_button_selector)
        break
        if next_page_button.is_enabled():
            next_page_button.click()
            time.sleep(2)
        else:
            #Reached last page
            break

def generate_file(result):
    with open(result_file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headerrow)
        for name in result:
            writer.writerow(result[name])

each_page()
generate_file(result)