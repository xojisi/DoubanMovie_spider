# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import urllib2
import os

class DoubanmoviesSpider(scrapy.Spider):
	name = 'doubanmovies'
	allowed_domains = ['douban.com']
	start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0']
	headers = {
		'Cookie':'''bid=yzKMwwSgFSI; ll="118291"; __utmt=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1495696955%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __yadk_uid=vdq90QCAt4Dm8ZeXRmKG85H1k1wwf5z5; _vwo_uuid_v2=F71ED78F725773FA338DF87F3EA3ACCD|ab63597699a0e2fa2b0e7205eb6dcd5b; __ads_session=Kia7f6ZA6gigm9wEBgA=; _pk_id.100001.4cf6=1cce0872d7a8a2f4.1495696955.1.1495696969.1495696955.; _pk_ses.100001.4cf6=*; __utma=30149280.1366897573.1495696952.1495696952.1495696952.1; __utmb=30149280.1.10.1495696952; __utmc=30149280; __utmz=30149280.1495696952.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1437948693.1495696955.1495696955.1495696955.1; __utmb=223695111.0.10.1495696955; __utmc=223695111; __utmz=223695111.1495696955.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/''',
		'Host': 'movie.douban.com',
		'Upgrade-Insecure-Requests':1,
		'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'''
	}
	
	def start_requests(self):
		yield scrapy.Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)
		
	def parse(self, response):
		json_dict = json.loads(response.body)

		for m in json_dict['subjects']:
		
			path = 'D:\\doubanmovie\\'+ m['title']

			if not os.path.exists(path):
				os.makedirs(path)

			urllib.urlretrieve(m['cover'],'D:\\doubanmovie\\%s\\%s.jpg'% (m['title'],m['title']))
			
		return
