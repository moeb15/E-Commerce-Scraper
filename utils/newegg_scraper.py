import pandas as pd
import time
import requests
from urllib.parse import quote
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.newegg.ca/p/pl?d='


class NeweggScraper:
    def __init__(self,BASE_URL,query):
        self.BASE_URL = BASE_URL
        self.query = query
        self.first_page = self.build_soup(self.BASE_URL,self.query,1)
        try:
            self.page_max = int(self.first_page.find('span',{'class':'list-tool-pagination-text'})\
                                .get_text().split("/")[1])
        except:
            self.page_max = 1

    def build_soup(self, BASE_URL,query,page):
        URL = BASE_URL + quote(query) + f'&page={page}'
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        webpage = requests.get(url=URL,headers=HEADERS,allow_redirects=True)
        if(webpage.status_code != 200):
            return f'Status Code {webpage.status_code}'
        return BeautifulSoup(webpage.content,'html.parser')
    
    def scrape_page(self,soup):
        res = soup.find('div',{'class':'list-wrap'})
        try:
            items = res.find_all('div',{'class':'item-cell'})
        except:
            items = None
        if items == None:
            return pd.DataFrame({'Product Name':[],
                            'Current Price':[],
                            'Sale Percentage':[]})

        prod_names = []
        prod_cur_price = []
        prod_sale_percent = []

        for item in items:
            product_desc = item.find('a',{'class':'item-title'})
            cur_price = item.find('li',{'class':'price-current'})
            save_percent = item.find('span',{'class':'price-save-percent'})
            
            prod_names.append(product_desc.get_text())
            prod_cur_price.append(cur_price.get_text())
            prod_sale_percent.append(save_percent.get_text() if save_percent != None else '0%')

        newegg_df = pd.DataFrame({'Product Name':prod_names,
                            'Current Price':prod_cur_price,
                            'Sale Percentage':prod_sale_percent})
        
        return newegg_df

    def paginated_scrape(self,limit):
        if limit == -1:
            limit = self.page_max
        
        newegg_df = pd.DataFrame({'Product Name':[],
                          'Current Price':[],
                          'Sale Percentage':[]})

        for k in range(1,limit+1):
            paginated_soup = self.build_soup(self.BASE_URL,self.query,k)
            df = self.scrape_page(paginated_soup)
            newegg_df = pd.concat([newegg_df,df],axis=0)
            time.sleep(3)

        newegg_df['Current Price'] = newegg_df['Current Price'].str.replace(r'[^0-9 \.]+', '', regex=True)
        
        return newegg_df


def extract_data(query):
    scraper = NeweggScraper(BASE_URL, query)
    df = scraper.paginated_scrape(-1)
    cur_date = datetime.now()
    fname = f'{query}-{cur_date}.csv'

    return df, fname