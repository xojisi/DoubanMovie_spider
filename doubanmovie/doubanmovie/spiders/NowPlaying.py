 # -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http.request import Request
from doubanmovie.items import NowPlayingItem


import sys
reload(sys)  
sys.setdefaultencoding('utf8')  
'''解决错误：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)'''


'''
使用Scrapy抓取豆瓣热门电影信息
包含:电影名,简介,海报URL,导演,演员等.
'''
class NowPlayingSpider(scrapy.Spider):
	name = 'NowPlaying'
	start_urls = ['https://movie.douban.com/cinema/nowplaying/shenzhen/']
	headers = {'User-Agent': '''Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36'''}

	custom_settings = {
		'ITEM_PIPELINES': {
			'doubanmovie.pipelines.NowPlayingSQLPipeline': 300,
		}
	}

	def __init__(self, *a, **kw):
		super(NowPlayingSpider, self).__init__(self.name, **kw)
		self.turn = a[0]
		self.logger.info("%s. this turn %d" % (self.name, self.turn))

	# 用函数的进行，对start_url加入headers信息
	def start_requests(self):
		yield Request(url=self.start_urls[0], headers=self.headers,callback=self.parse,meta = {"turn":self.turn})

	# 爬取start_urls中的所有城市信息，并遍历所有城市页面，爬去所有城市页面中的所有正在上映的电影信息。
	def parse(self, response):
		# 获取所有城市的页面代码
		all_city = response.xpath('//dl[@class="city-mod"]/dd/span/a/@uid').extract()
		# 遍历所有城市页面
		for m in all_city:
			self.url  = 'https://movie.douban.com/cinema/nowplaying/' + m + '/'
			yield Request(url=self.url,headers=self.headers,callback=self.parse_city,meta = {"turn":response.meta["turn"]},dont_filter=True)

	# 爬取当前城市页面中的所有正在上映电影的详细页URL
	def parse_city(self, response):

		# 获取这个页面所有的电影ID，用于电影详细页的url生成
		movie_id = response.xpath('//div[@id="nowplaying"]/div/ul/li/@id').extract()
		for m in movie_id:
			# 每次循环后实例化一次，清空item
			item = NowPlayingItem()
			item["city"] = re.findall('<h1 class="page-title">电影票 - (.*?)</h1>', response.body)[0]
			self.url = 'https://movie.douban.com/subject/' + m +'/'
			yield Request(url=self.url,headers=self.headers,meta={'item':item,"turn":response.meta["turn"]},callback=self.parse_detail,dont_filter=True)

	# 爬取电影详细页中的信息
	def parse_detail(self,response):

		# 接受parse_city函数传过来的item
		item = response.meta['item']

		# 电影ID
		item['movie_id'] = response.xpath('//span[@class="rec"]/a/@data-url')[0].extract().\
			replace('https://movie.douban.com/subject/', '').replace('/', '')
		# 抓电影名
		item["movie_name"] = re.findall(r'<title>\s*(.*?)\s*\(豆瓣\)\s*</title>', response.body)[0]
		# 抓电影海报URL
		item['movie_img_url'] = response.xpath("//img[@rel='v:image']/@src")[0].extract()
		# 抓电影评分
		try:
			item['movie_score'] = response.xpath('//strong[@property="v:average"]/text()')[0].extract()
		except:
			item['movie_score'] = ''
		# 抓电影导演
		item["movie_director"] = response.xpath("//*[@id='info']/span/span/a[@rel='v:directedBy']/text()").extract()
		item["movie_director"] = '/'.join(item["movie_director"])
		# 抓电影演员
		item["movie_performer"] = response.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a/text()').extract()
		item["movie_performer"] = '/'.join(item["movie_performer"])
		# 抓电影类型
		item["movie_type"] = response.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract()
		item["movie_type"] = '/'.join(item["movie_type"])
		# 抓制片国/地区
		item["movie_region"] =  re.findall(r'制片国家/地区:</span>\s*(.*?)\s*<br/>', response.body)
		item["movie_region"] = '/'.join(item["movie_region"])
		# 抓上映时间
		item['movie_release_date'] = response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
		item['movie_release_date'] = '/'.join(item['movie_release_date'])
		# 抓电影年份
		item["movie_year"] = response.xpath("//span[@class='year']/text()")[0].extract().\
			replace('(', '').replace(')','')
		# 抓电影简介
		if response.xpath('//*[@id="link-report"]') != []:
			try:
				item["movie_intro"] = response.xpath('//*[@id="link-report"]/span[@class="short"]/span')[0].\
					extract().replace('<span property="v:summary" class="">', '').\
					replace('<span property="v:summary">','').replace('<br>','').replace('</span>', '').strip()
			except:
				item["movie_intro"] = response.xpath('//*[@id="link-report"]/span')[0].extract().\
					replace('<span property="v:summary"', '').replace(' class="">', '')\
					.replace('<br>', '').replace('</span>','').strip()
		else:
			# 解决没有电影简介的情况
			item["movie_intro"] = ''

		item["turn"] = response.meta["turn"]

		yield item

