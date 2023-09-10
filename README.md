# E-Commerce Product Data Scraper
For this project I utilized one of the webscrapers I created for scraping 
product data from Newegg Canada for a given search query, this project adds to the previous one by including a web app users can interact with inorder to scrape product data and download the data as a csv.  

Currently the project supports scraping from Newegg Canada, in the future I'd like to add support for Amazon and Canada Computers. I've deployed the application on Google Cloud Platform using Cloud Run, although I need to obtain a pool of proxy IP addresses given that the sites are automatically blocking my webscraper, which makes sense seeing as it can just immediately regard Datacenter IPs as non-authentic users. You can the access the application at the following [link](https://ecom-app-4ol4gxt7cq-uc.a.run.app).
