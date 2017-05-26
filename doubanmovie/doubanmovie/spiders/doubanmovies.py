# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import urllib2
import os
from doubanmovie.items import DoubanmovieItem

import sys
reload(sys)  
sys.setdefaultencoding('utf8')  
'''解决错误：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)'''


'''
使用Scrapy抓取豆瓣电影简介，简介信息图片，要求:分类必须明确,某一部电影信息，都需要创建一个文件夹单独存放。
'''
class DoubanmoviesSpider(scrapy.Spider):
	name = 'doubanmovies'
	allowed_domains = ['douban.com']
	# json
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
		
			item = DoubanmovieItem()
			# 电影名
			item["movie_name"] = m['title']
			# 电影详细页面url
			item["movie_detail_url"] = m['url']
			# 电影评分
			item["movie_score"] = m['rate']
			# 电影存放至本地文件夹的路径
			item['movie_path'] = 'D:\\doubanmovie\\'+ m['title']
			# 电影简介txt的存放路径
			item['movie_summary_path'] = 'D:\\doubanmovie\\'+ m['title'] + '\\summary.txt'
			# 电影图片的存放路径
			item['movie_img_path'] = 'D:\\doubanmovie\\'+ m['title'] + '\\'+ m['title'] + '.jpg'
			# 电影图片URL
			item['movie_img_url'] = m['cover']

			#判断电影（信息）存在的路径是否存在
			if not os.path.exists(item['movie_path']):
				os.makedirs(item['movie_path'])

			#抓电影图片
			urllib.urlretrieve(item['movie_img_url'],item['movie_img_path'])

			#将josn中的评分、电影名信息写入
			with open(item['movie_summary_path'],'a+') as f:
				f.write('电影名:'+item["movie_name"]+'\n'+'评分:'+item["movie_score"]+'\n')

			
			yield scrapy.Request(url=item["movie_detail_url"],meta={'item':item}, headers=self.headers,callback=self.parse_detail,
            dont_filter=True)
	
	def parse_detail(self,response):
		item = response.meta['item']

		# 抓电影导演
		item["movie_director"] =  response.xpath("//*[@id='info']/span/span/a[@rel='v:directedBy']/text()")[0].extract()
		# 抓电影演员
		item["movie_performer"] =  response.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a/text()').extract()
		# 抓电影类型
		item["movie_type"] = response.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract()

		# 抓电影简介
		try:
			item["movie_info"] = response.xpath('//*[@id="link-report"]/span[@class="short"]/span')[0].extract().replace('<span property="v:summary" class="">','').replace('<span property="v:summary">','').replace('<br>','').replace('</span>','').replace('   ','')
		except:
			item["movie_info"] = response.xpath('//*[@id="link-report"]/span')[0].extract().replace('<span property="v:summary"','').replace(' class="">','').replace('<br>','').replace('</span>','').replace('   ','')

		#写入导演、主演、类型、简介等信息
		with open(item['movie_summary_path'],'a+') as f:
			#导演
			f.write('导演:' + item["movie_director"]+'\n')

			#主演
			f.write('主演:')
			for t in item['movie_performer']:
				f.write(t + '|')
			f.write('\n')

			#类型
			f.write('类型:')
			for ty in item['movie_type']:
				f.write(ty + '|')
			f.write('\n')

			#简介
			f.write('简介:' + item["movie_info"])

		yield item