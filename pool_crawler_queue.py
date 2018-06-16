from multiprocessing import Pool 
from mongo_queue_p3 import MongoQueue
from mongo_cache_p3 import MongoCache 
from scrape_callback_p3 import Scrape_Callback
from downloader_p3 import Downloader
import threading
import urllib.parse
import multiprocessing
import time 
import os
import lxml.html
import re

SLEEP_TIME = 2
DEFAULT_CACHE = MongoCache()
DEFAULT_SC_CALLBACK = Scrape_Callback()
def threaded_crawler(pages,delay=2,cache=DEFAULT_CACHE,scrape_callback=DEFAULT_SC_CALLBACK,user_agent='wswp',proxies=None,num_retries=1,max_threads=10,timeout=60):
	crawl_queue = MongoQueue()
	crawl_queue.clear()
	D = Downloader(cache=cache,delay=delay,num_retries=num_retries,timeout=timeout)
	for page in range(1,pages+1):
		stock_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={}&size=90&order=desc&orderby=percent&type=11%2C12'.format(page)
		crawl_queue.push(stock_url)
	def process_queue():
		while True:
			try:
				url = crawl_queue.pop()
			except KeyError:
				break
			else:
				response = D(url)
				if scrape_callback:
					scrape_callback.__call__(response)
				crawl_queue.complete(url)
	process_queue()

def pool_crawler(args):
	num_cpu = multiprocessing.cpu_count()
	pool = Pool(4)
	print('Start {} processing'.format(num_cpu))
	for num in range(4):
		#print('kwargs=',kwargs)
		pool.apply_async(func=threaded_crawler,args=(args,))
	pool.close()
	pool.join()





