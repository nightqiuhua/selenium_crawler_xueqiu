import re 
import urllib.parse 
import urllib.request 
import datetime 
import time 
from downloader_p3 import Downloader
from mogon_cache import MongoCache
from scrape_callback2_p3 import Scrape_Callback
import lxml.html 


def link_crawler(seed_url,delay=5,num_retries=1,scrape_callback=None,cache=None):
	D= Downloader(delay=delay,num_retries=num_retries,cache=cache)
	page_number = get_total_pages(seed_url,D)
	for page in range(1,page_number+1):
		stock_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={}&size=90&order=desc&orderby=percent&type=11%2C12'.format(page)
		try:
			html = D(stock_url)
		except Exception as e:
			raise e
		else:
			if scrape_callback:
				scrape_callback.__call__(html)

def get_total_pages(seed_url,Downloader):
	page_html = Downloader(seed_url)
	data_regx = re.compile('<pre style="word-wrap: break-word; white-space: pre-wrap;">(.*?)</pre>',re.IGNORECASE)
	data = data_regx.findall(page_html)
	data_dict = eval(data[0])
	total_number = data_dict['count']['count']
	page_number = total_number//90 +1
	return page_number



seed_url ='https://xueqiu.com/stock/cata/stocklist.json?page=1&size=90&order=desc&orderby=percent&type=11%2C12'

link_crawler(seed_url=seed_url,scrape_callback=Scrape_Callback(),cache = MongoCache())