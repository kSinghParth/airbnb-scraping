# airbnb-scrapping
## A scrapping bot to list hotels from Boston


![Test Image](/images/airbnb_home.png)

1. Airbnb does not provide an official API that can be used by developers. However, the frontend does utilize API to populate the data. This can be seen from the Web Inspector.

2. There are multiple projects on GitHub which exploit this. After trying out a few of those projects, I realized that they are older APIs that Airbnb uses. Airbnb updates their APIs frequently which results in these projects breaking. These projects required the user to provide their API_KEY. This key could be found in the Network tab of Web Inspector. But with the latest API calls version that Airbnb is using, although you can find your API_KEY, you cannot use it for the search query. Airbnb seems to be using an OAuth kind of mechanism to grant access to its data.

Example on a project which used the older version of API- https://github.com/digital-engineering/airbnb-scraper

Therefore, to fetch data, the only option left at this point is to scrap the HTML.

3. Initially decide to use Scrapy. It is much faster than selenium because it doesn't render the page on any browser. The scrappy shell also helps in quickly figuring out HTML elements structure and

4. Using Scrapy:

Scrapy seemed like the next best option. But Airbnb is a Single Page Application. Most of the content of the page is loaded dynamically by JS(this is why unofficial APIs are available in the first place), which is why Scrapy is unable to read it. Scrapy cannot render dynamic data, unfortunately.

5. Now I'll have to do something, which I was trying to avoid from the very beginning. Selenium.

6. Airbnb only shows 20 results per page and 15 pages at max. Therefore if we need to scrape more than 300 entries in any area, we will have to partition the search area into smaller areas.

Each time I see that a search area has more than 300 listings, I partition the area into 4 quarters and then search those individually. If any of those 4 quarters contain more than 300 entries, it will be partitioned further, and so on. Recursion-ion-ion-ion.

Since, with latitude longitude boundaries, I can only parse rectangular areas, please see different ways to cover Boston.

![Boston covered area with blocks](/images/covered_area_blocks.png)
![Boston covered area with single block](/images/covered_area_single.png)


7. Finally, Airbnb will likely block an IP if used too often, so I had to rotate IP using proxies.
I used a couple of libraries like FreeProxya and http_request_randomizer and even directly queried sslproxies.org, but those IPs greatly increased the latency to the point that some requests with timing out. I tried using elite IPs but didn't solve the problem either. Airbnb was not opening at all for certain regions altogether. Requests were straight away denied. Perhaps a paid IP Proxy service, like zyte.org will help here.

8. A little something I added extra to the project.
The ultimate goal of the project is not to scrape Boston, but all of the United States. The script will run for a considerable amount of time and there are numerous network calls involved (Airbnb, proxies), any of which can fail because of various reasons. Right now the primary reason for failure was timeouts by proxy service.

For this reason, I have added support for Persistent Searching. I have used Memoization, and have stored the data that has already been parsed. We cannot be parsing all the coordinates every time.

This feature of Persistent Searching can be disabled by setting

persistent_searching: False
in conf.yaml

If enabled, it will not process locations that the scrapper has already processed.

9. The application has DEBUG level logging setup.



## Installation

1. Create virtual environment.
```shell
virtualenv venv
```
2. Start virtual environment.
```Shell
source venv/bin/activate
```
3. If your chrome driver location is set as an environment variable, you dont need to worry.
If not, please go ahead and change the location in conf.yaml.
`chrome_driver`

You will also have to uncomment the lines 69-73 in script.py

4. Set Persistent Searching in conf.yaml as per your requirement. True/False.

5. Run project
```Shell
python script.py

```


Note: Even if the script crashes at any point, you don't need to worry, simply run it again, and it won't search the previously parsed latitudes and longitudes.

## Outcome

I parsed Boston city with two approaches.

1. With a single big rectangular block. This also included certain areas not in Boston.

![Boston covered area with single block](/images/covered_area_single.png)

	Number of Listings returned = 3707

	You can find the list here: https://github.com/kSinghParth/airbnb-scrapping/blob/main/listing_in_boston_single.csv

2. With multiple smaller blocks to keep the search results strictly within Boston.

![Boston covered area with blocks](/images/covered_area_blocks.png)

	Number of Listings returned = 3113

	You can find the list here: https://github.com/kSinghParth/airbnb-scrapping/blob/main/listing_in_boston_blocks.csv