import re
import pymongo
from pymongo import MongoClient,errors


class Scrape_Callback:
	def __init__(self):
		self.db = pymongo.MongoClient("localhost", 27017).cache

	def __call__(self,html):
		#html = Downloader(url).decode('utf-8')
		data_regx = re.compile('<pre style="word-wrap: break-word; white-space: pre-wrap;">(.*?)</pre>',re.IGNORECASE)
		data = data_regx.findall(html)
		data_dict = eval(data[0])
		for item in data_dict['stocks']:
			item['_id'] = item['symbol']
			try:
				self.db.stocks.insert(item)
			except errors.DuplicateKeyError as e:
				pass
