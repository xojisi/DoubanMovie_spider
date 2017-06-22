# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http.request import Request
from doubanmovie.items import NewMovieItem


import sys
reload(sys)  
sys.setdefaultencoding('utf8')  
'''解决错误：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)'''


'''
使用Scrapy抓取豆瓣热门电影信息
包含:电影名,简介,海报URL,导演,演员等.
'''
class NewMovieSpider(scrapy.Spider):
	name = 'NewMovie'
	start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=1000&page_start=0']
	headers = {'User-Agent': '''Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'''}
	custom_settings = {
		'ITEM_PIPELINES': {
			'doubanmovie.pipelines.NewMovieSQLPipeline': 300,
		}
	}

	def __init__(self, *a, **kw):
		super(NewMovieSpider, self).__init__(self.name, **kw)
		self.turn = a[0]
		self.logger.info("%s. this turn %d" % (self.name, self.turn))

	# 用函数的进行，对start_url加入headers信息
	def start_requests(self):
		yield Request(url=self.start_urls[0], headers=self.headers,callback=self.parse,meta = {"turn":self.turn})

	# 解析start_requests传过来的url
	def parse(self, response):

		# 因为传过来的URL是JSON文件，所以需要转换
		json_dict = json.loads(response.body)

		# 遍历JSON
		for m in json_dict['subjects']:

			# 每次循环后都重新实例化，清空item
			item = NewMovieItem()
			# 电影ID
			item['movie_id'] = m['id']
			# 电影名
			item["movie_name"] = m['title']
			# 电影详细页面url
			item["movie_detail_url"] = m['url']
			# 电影评分
			item["movie_score"] = m['rate']
			# 电影海报URL
			item['movie_img_url'] = m['cover']

			yield Request(url=item["movie_detail_url"],headers=self.headers,meta={'item':item,"turn":response.meta["turn"]},callback=self.parse_detail)
	
	def parse_detail(self,response):

		# 接受parse函数传过来的meta
		item = response.meta['item']

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
		try:
			item["movie_intro"] = response.xpath('//*[@id="link-report"]/span[@class="short"]/span')[0].extract().replace('<span property="v:summary" class="">','').replace('<span property="v:summary">','').replace('<br>','').replace('</span>','').strip()
		except:
			item["movie_intro"] = response.xpath('//*[@id="link-report"]/span')[0].extract().replace('<span property="v:summary"','').replace(' class="">','').replace('<br>','').replace('</span>','').strip()

		item["turn"] = response.meta["turn"]

		yield item

