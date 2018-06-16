import sys
from pool_crawler_queue import pool_crawler
from mongo_cache_p3 import MongoCache
from downloader_p3 import Downloader
import re


def main(max_threads):
	seed_url = 'https://xueqiu.com/stock/cata/stocklist.json?page=1&size=90&order=desc&orderby=percent&type=11%2C12'
	cache = MongoCache()
	D = Downloader(cache=cache)
	page_number = get_total_pages(seed_url,D)
	print(page_number)
	pool_crawler(page_number)


def get_total_pages(seed_url,Downloader):
	page_html = Downloader(seed_url)
	data_regx = re.compile('<pre style="word-wrap: break-word; white-space: pre-wrap;">(.*?)</pre>',re.IGNORECASE)
	data = data_regx.findall(page_html)
	data_dict = eval(data[0])
	total_number = data_dict['count']['count']
	page_number = total_number//90 +1
	return page_number


if __name__ == '__main__':
	main()
