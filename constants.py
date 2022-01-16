import urllib.parse

next_button_selector = '._1bfat5l'
listings_selector = '.ltlgcp'
listing_name_selector = '.k1pnia7m.dir.dir-ltr'
listing_rating_selector = '.s1hj3bst.dir.dir-ltr'

city_name = 'Boston, MA, United States'
city_code = 'Boston--MA--United-States'

search_url = 'https://www.airbnb.com/s/' + city_code + '/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=' + urllib.parse.quote(city_name) + '&place_id=ChIJGzE9DS1l44kRoOhiASS_fHg'

coordinates = [
		{'ne_lat': '42.37247755007246', 'ne_lng': '-71.012691', 'sw_lat': '42.290420','sw_lng': '-71.113040'}
	]

result_file_name = 'listing_in_boston.csv'
coordinate_lookup_file_name = 'coordinate_lookup.json'