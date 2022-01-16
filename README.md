# airbnb-scrapping
A scrapping bot to pick hotels from Boston


Airbnb does not provide an official API which can be used by developers. However, the frontend does utilize API to populate the data. This can be seen from the Web Inspector.

There are multiple projects on github which exploit this. After trying out a few of those projects, I realized that they are older APIs which Airbnb uses. Airbnb updates thier APIs frequently which results in these projects to break. These projects relied on the user providing it the API_KEY. This key could be found in the Network tab of Web Inspector. But with the latest API calls, though you can find your API_KEY, you cannot use it for the search query. Airbnb seems to be using an OAuth kind of mechanism to grant access to it's data.

Example on a project which used the older version of API- https://github.com/digital-engineering/airbnb-scraper

Therefore, to fetch data, the only option left at this point is to scrap the HTML.


I will be using Scrapy for the same.


Using Scrapy:

Scrapy seemed like the next best option. But Airbnb is a Single Page Application. Most of the content of the page is loaded dynamically by JS(this is why unofficial APIs are avialbale in the first place), which is why Scrapy is unabel to read it.


Now I'll have to do something, which I was trying to avoid from the very beginning.
Selenium.



Airbnb only shows 20 results per page and 15 pages at max. Therefore if we need to scrape more than 300 entries, we will have to partition the target area based on latitude and longitude.



Problem: IP is very slow. Conenction to airbnb not working.




adding support for persistent searchibng. There can be multiple reasons for the program to crash, IP proxy being the primary one. For such cases we need to store the data that has already been parsed. We canniot be parsing all the coordinated everytime. Here we are performing memoization.	