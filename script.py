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

next_button = '//*[@id="site-content"]/div[4]/div/div/div'
listing = '.ltlgcp'

def each_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    driver.find_element(By.XPATH,next_button).click()
    time.sleep(10)
    listings = driver.find_elements(By.CSS_SELECTOR,'.ltlgcp')
    print(len(listings))
    for list in listings:
        print(list)
    driver.find_element(By.XPATH,next_button).click()

    time.sleep(20)

each_page()
exit()



# print("Starting search")
# inp_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
# search=driver.find_element(by=By.XPATH, value=inp_xpath_search)
# time.sleep(3)
# search.click()
# time.sleep(3)
# print("waiting done")

# with open('numbers', 'r') as numbers:
#     nums= numbers.readlines()
#     for n in nums:
#         contact=n.strip()[1:-2].strip()
#         #contact='Gandarhv'
#         #print(n.strip()[1:-1])
#         search.send_keys(contact)
#         time.sleep(3)
#         time.sleep(3)
#         message = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
#         time.sleep(3)
#         message.send_keys(text +Keys.ENTER)
#         #driver.find_element(by=By.XPATH, value='//*[@id="pane-side"]/div[1]/div/div/div[6]/div/div/div[2]').click()
#         time.sleep(3)
#         search.clear()
# print("Ending...")
