import urllib.request 
import urllib.parse 
import socket 
from datetime import datetime 
import time 
import random
import gzip
import re
import json
from selenium import webdriver


DEFAULT_DELAY = 2
DEFAULT_TIMEOUT = 200
DEFAULT_RETRIES = 1
DEFAULT_CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
DEFAULT_SEED_URL = 'https://xueqiu.com/hq'


class Throttle:
	def __init__(self,delay):
		self.delay = delay
		self.domains = {}

	def wait(self,url):
		domain = urllib.parse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay > 0 and last_accessed is not None:
			sleep_sec = self.delay-(datetime.now() - last_accessed).seconds
			if sleep_sec>0:
				time.sleep(sleep_sec)
		self.domains[domain] = datetime.now()

class Downloader:
	def __init__(self,delay=DEFAULT_DELAY,proxies=None,num_retries=DEFAULT_RETRIES,timeout=DEFAULT_TIMEOUT,driver_path=DEFAULT_CHROME_PATH,seed_url=DEFAULT_SEED_URL,cache=None):
		socket.setdefaulttimeout(timeout)
		self.throttle = Throttle(delay)
		self.num_tries=num_retries
		self.cache = cache
		self.driver = webdriver.Chrome(driver_path)
		self.seed_url = seed_url


	def __call__(self,url):
		result = None
		if self.cache:
			try:
				result = self.cache[url]
			except KeyError:
				pass
			else:
				if self.num_tries > 0 and 500<= result['code'] <600:
					result = None
		if result is None:
			self.throttle.wait(url)
			result = self.download(url,s_url=self.seed_url,num_tries=self.num_tries)
			if self.cache:
				self.cache[url] = result
		#print(result['html'])
		return result['html']

	def download(self,url,s_url,num_tries):
		print('Downloading seed url:',s_url)
		self.driver.get(s_url)
		time.sleep(3)
		print('Downloading:',url)
		try:
			#发送请求
			self.driver.get(url)
			time.sleep(2)
			html = self.driver.page_source
			code = 200
		except Exception as e:
			print('Download error',e)
			html = ' '
			if hasattr(e,'code'):
				code = e.code
				if num_tries>0 and 500<=code<600:
					html = self.download(url,num_tries-1)
			else:
				code = -1
		#self.driver.close()
		return {'html':html,'code':code}

if __name__ == '__main__':
	seed_url = 'https://xueqiu.com/stock/cata/stocklist.json?page=3&size=90&order=desc&orderby=percent&type=11%2C12'
	D = Downloader()
	html = D(url=seed_url)
	print('html=',html)
	print('type(html)',type(html))


