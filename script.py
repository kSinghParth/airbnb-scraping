from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import yaml


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# try:
#     with open("conf.yaml", 'r') as stream:
#         chrome_driver = yaml.safe_load(stream).get('chrome_driver')
# except:
    # print('Unable to read driver location')
chrome_driver = os.environ.get('CHROME_DRIVER')
driver=webdriver.Chrome(executable_path=chrome_driver)

response = []

driver.get('https://www.airbnb.com/s/Boston--MA--United-States/homes?place_id=ChIJGzE9DS1l44kRoOhiASS_fHg&refinement_paths%5B%5D=%2Fhomes&adults=0&children=0&infants=0&pets=0&search_type=AUTOSUGGEST')

time.sleep(10)
next_button = '._1bfat5l'
listing = '.ltlgcp'
name=".k1pnia7m.dir.dir-ltr"
rating = ".s1hj3bst.dir.dir-ltr"
rating2=".b1odgil1.dir.dir-ltr div"
def each_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    # time.sleep(10)
    listings = driver.find_elements(By.CSS_SELECTOR,listing)
    print(len(listings))
    for list in listings:
        print(list.find_element(By.CSS_SELECTOR,name).text)
        try:
            print(list.find_element(By.CSS_SELECTOR,rating).text)
        except:
            print("No rating")
        print()
        


    # driver.find_element(By.CSS_SELECTOR,next_button).click()
    # time.sleep(20)

each_page()
exit()

