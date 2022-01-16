from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fp.fp import FreeProxy
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

import os
import time
import yaml
import csv
import json
import re
import logging
import datetime

# import chromedriver_autoinstaller # pip install chromedriver-autoinstaller
# chromedriver_autoinstaller.install()

from constants import next_button_selector, listings_selector, listing_id_regex,listing_name_selector, listing_rating_selector, result_file_name, search_url, coordinates, coordinate_lookup_file_name, listing_id_selector


logging.basicConfig(filename='logs/airbnb_scapper_' + str(datetime.datetime.now()) + '.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

#Result object
result = {}
stored_result = {}
stored_coordinate_searched = []
coordinates_searched = []
persistent_searching = True
headerrow = ['Id','Name and Description', 'Rating']

# # Trying out different free proxy
#
# try:
#     #Fetching proxies
#     req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
#     proxies = req_proxy.get_proxy_list() #this will create proxy list
#     logging.info(proxies[0])
# except:
#     pass

def itr_search(coordinates):

    try:
        PROXY = FreeProxy(country_id=['US', 'ID', 'JP', 'MX', 'FR', 'IN', 'BR', 'SG', 'DE'], timeout=1, rand=True).get()
        logging.info('Proxy selected: ' + PROXY)
    except:
        logging.info('No proxies found')
        PROXY = None
    # Setting proxy
    webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpsProxy":PROXY,
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "proxyType":"MANUAL",
    }

    # # Driver setup
    
    # # I have saved my driver location as an environment variable. 
    # # Other users can save it in conf.yaml file and un-comment this snippet.
    
    # try:
    #     with open("conf.yaml", 'r') as stream:
    #         chrome_driver = yaml.safe_load(stream).get('chrome_driver')
    # except:
    #     logging.info('Unable to read driver location')

    # # Getting driver location from env variable
    chrome_driver = os.environ.get('CHROME_DRIVER')
    driver=webdriver.Chrome(executable_path=chrome_driver)

    # # Testing IP Proxy
    # driver.get('https://www.expressvpn.com/what-is-my-ip')
    # time.sleep(20)

    for coordinate  in coordinates:
        if is_coordinate_search_allowed(coordinate):
            logging.info('----------' + coordinate_string(coordinate) + ' starting search.')
            grid_search_and_divide(coordinate, driver)
            logging.info('==========' + coordinate_string(coordinate) + 'completed search.')
        else:
            logging.info('xxxxxxxxxx' + coordinate_string(coordinate) + ' is already covered.')

    # driver.close()

def coordinate_string(coordinate):
    return coordinate['ne_lat']+','+coordinate['ne_lng']+','+coordinate['sw_lat']+','+coordinate['sw_lng']

def is_coordinate_search_allowed(coordinate):
    cdnt_string = coordinate_string(coordinate)
    if cdnt_string in coordinates_searched: 
        return False
    if persistent_searching:
        if cdnt_string in stored_coordinate_searched:
            return False
    return True


def is_listing_allowed(listing_id):
    if listing_id in result: 
        return False
    if persistent_searching:
        if listing_id in stored_result:
            return False
    return True

def parse_id(attr_id):
    try:
        # two groups enclosed in separate ( and ) bracket
        result = re.search(listing_id_regex, attr_id)

        return result.group(2)
    except:
        logging.info('Exception occured while extarcting id')
        return attr_id

def grid_search_and_divide(coordinate, driver):
    complete_url = search_url
    for key in coordinate:
        complete_url = complete_url + '&' + key + '=' + coordinate[key]

    #Starting the driver
    driver.get(complete_url)

    #Allow loading time for the whole page to render. Since Airbnb is a SPA, a lot of backend calls are involved
    time.sleep(7)

    results_added = each_page(driver)

    logging.info("Results from coordinates: " + str(results_added))
    if results_added >= 300 :
        logging.info("Diving further " + coordinate_string(coordinate))
        mid_lat = (float(coordinate['ne_lat']) + float(coordinate['sw_lat']))/2
        mid_lng = (float(coordinate['ne_lng']) + float(coordinate['sw_lng']))/2
        new_coorindates = [
            {'ne_lat': coordinate['ne_lat'], 'ne_lng': coordinate['ne_lng'], 'sw_lat': str(mid_lat),'sw_lng': str(mid_lng)},
            {'ne_lat': str(mid_lat), 'ne_lng': str(mid_lng), 'sw_lat': coordinate['sw_lat'],'sw_lng': coordinate['sw_lng']},
            {'ne_lat': coordinate['ne_lat'], 'ne_lng': str(mid_lng), 'sw_lat': str(mid_lat),'sw_lng': coordinate['sw_lng']},
            {'ne_lat': str(mid_lat), 'ne_lng': coordinate['ne_lng'], 'sw_lat': coordinate['sw_lat'],'sw_lng': str(mid_lng)},
        ]
        itr_search(new_coorindates)

    coordinates_searched.append(coordinate_string(coordinate))


def each_page(driver):
    local_listing_count = 0
    while True:
        #Scrolling to the bottom of the page, for the next button to render
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);")
        time.sleep(1)
        
        #Selecting a list of all listings on this page
        listings = driver.find_elements(By.CSS_SELECTOR,listings_selector)
        
        for list in listings:
            listing_id = parse_id(list.find_element(By.CSS_SELECTOR,listing_id_selector).get_attribute("id"))
            if is_listing_allowed(listing_id):
                try:
                    name_of_listing = list.find_element(By.CSS_SELECTOR,listing_name_selector).text
                    rating_of_listing = list.find_element(By.CSS_SELECTOR,listing_rating_selector).text
                except:
                    #Listing does not have a rating
                    rating_of_listing = 'No Rating'
                    logging.info(listing_id + ' has no rating')
                result[listing_id] = [listing_id, name_of_listing, rating_of_listing]
                local_listing_count = local_listing_count + 1
                logging.info('Added listing: ' + listing_id)
        
        try:
            #Handling pagination of results    
            next_page_button = driver.find_element(By.CSS_SELECTOR,next_button_selector)
            if next_page_button.is_enabled():
                next_page_button.click()
                time.sleep(4)
            else:
                #Reached last page
                break
        except:
            logging.info("No paginmation exists")
            break
    return local_listing_count

def generate_file(result):
    add_header = False
    if os.path.exists(result_file_name)==False or len(stored_result)==0:
        add_header = True

    if  persistent_searching==False:
        mode = 'w'
        add_header = True
    else:
        mode = 'a'

    with open(result_file_name, mode) as f:
        writer = csv.writer(f)
        if add_header:
            writer.writerow(headerrow)
        for id in result:
            writer.writerow(result[id])
    with open(coordinate_lookup_file_name, 'w') as f:
        coordinates_searched.extend(stored_coordinate_searched)
        json.dump(coordinates_searched, f)

def read_file():
    global stored_coordinate_searched
    if os.path.exists(result_file_name):
        try:
            with open(result_file_name, 'r') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    stored_result[row[0]] = [row[0], row[1], row[2]]
        except Exception as e:
            logging.info(e)
            logging.info("Unable to open result file. Probably file does not exist.")


    if os.path.exists(coordinate_lookup_file_name):
        try:
            with open(coordinate_lookup_file_name, 'r') as f:
                stored_coordinate_searched.extend(json.load(f))
        except Exception as e:
            logging.info(e)
            logging.info("Unable to open coordinate lookup file. Probably file does not exist.")
    
if __name__ == "__main__":
    try:
        with open("conf.yaml", 'r') as stream:
            persistent_searching = yaml.safe_load(stream).get('persistent_searching')
    except:
        logging.info('Unable to read persistent searching flag. Default set to True.')

    if persistent_searching:
        read_file()

    try:
        itr_search(coordinates)
    except Exception as  e:
        logging.info('Exception occured')
        logging.info(e)
        
    generate_file(result)

