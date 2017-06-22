 # -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http.request import Request
from doubanmovie.items import UpComingItem


import sys
reload(sys)  
sys.setdefaultencoding('utf8')  
'''解决错误：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)'''


'''
使用Scrapy抓取豆瓣热门电影信息
包含:电影名,简介,海报URL,导演,演员等.
'''
class UpComingSpider(scrapy.Spider):
	name = 'UpComing'

	start_urls = ['https://movie.douban.com/coming']
	headers = {'User-Agent': '''Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWe bKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'''}

	custom_settings = {
		'ITEM_PIPELINES': {
			'doubanmovie.pipelines.UpComingSQLPipeline': 300,
		}
	}

	def __init__(self, *a, **kw):
		super(UpComingSpider, self).__init__(self.name, **kw)
		self.turn = a[0]
		self.logger.info("%s. this turn %d" % (self.name, self.turn))

	# 用函数的进行，对start_url加入headers信息
	def start_requests(self):
		yield Request(url=self.start_urls[0], headers=self.headers,callback=self.parse,meta = {"turn":self.turn})

	# 爬取start_url中的所有电影详细页url
	def parse(self, response):
		# 获取所有电影详细页url
		movie_detail_url = response.xpath('//a[@class=""]/@href').extract()

		# 遍历所有URL
		for self.url in movie_detail_url:
			yield Request(url=self.url, headers=self.headers, callback=self.parse_detail ,meta={"turn":response.meta["turn"]})

	# 爬取电影详细页中的所有信息
	def parse_detail(self,response):

		# 每次循环前实例化一次，清空item
		item = UpComingItem()
		# 电影ID
		item['movie_id'] = response.xpath('//span[@class="rec"]/a/@data-url')[0].extract().replace('https://movie.douban.com/subject/','').replace('/','')
		# 抓电影名
		item["movie_name"] = re.findall(r'<title>\s*(.*?)\s*\(豆瓣\)\s*</title>',response.body)[0]
		# 抓电影海报URL
		item['movie_img_url'] = response.xpath("//img[@rel='v:image']/@src")[0].extract()
		# 抓电影导演
		item["movie_director"] =  response.xpath("//*[@id='info']/span/span/a[@rel='v:directedBy']/text()").extract()
		item["movie_director"] = '/'.join(item["movie_director"])
		# 抓电影演员
		item["movie_performer"] =  response.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a/text()').extract()
		item["movie_performer"] = '/'.join(item["movie_performer"])
		# 抓电影类型
		item["movie_type"] = response.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract()
		item["movie_type"] =  '/'.join(item["movie_type"])
		# 抓制片国/地区
		item["movie_region"] =  re.findall(r'制片国家/地区:</span>\s*(.*?)\s*<br/>', response.body)
		item["movie_region"] = '/'.join(item["movie_region"])
		# 抓上映时间
		item['movie_release_date'] = response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
		item['movie_release_date'] = '/'.join(item['movie_release_date'])
		# 抓电影年份
		item["movie_year"] = response.xpath("//span[@class='year']/text()")[0].extract().replace('(','').replace(')','')

		# 抓电影简介
		if response.xpath('//*[@id="link-report"]') != []:
			try:
				item["movie_intro"] = response.xpath('//*[@id="link-report"]/span[@class="short"]/span')[0]. \
					extract().replace('<span property="v:summary" class="">', ''). \
					replace('<span property="v:summary">', '').replace('<br>', '').replace('</span>', '').strip()
			except:
				item["movie_intro"] = response.xpath('//*[@id="link-report"]/span')[0].extract(). \
					replace('<span property="v:summary"', '').replace(' class="">', '') \
					.replace('<br>', '').replace('</span>', '').strip()
		else:
			item["movie_intro"] = ''

		item["turn"] = response.meta["turn"]

		yield item

