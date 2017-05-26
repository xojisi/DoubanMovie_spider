# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	
	#电影评分
	movie_score = scrapy.Field()

	#电影详细页面url
	movie_detail_url = scrapy.Field()

	#电影演员
	movie_performer = scrapy.Field()

	#电影导演
	movie_director = scrapy.Field()

	#电影简介
	movie_info = scrapy.Field()

	#电影存放至本地文件夹的路径
	movie_path = scrapy.Field()

	#电影简介txt的存放路径
	movie_summary_path = scrapy.Field()

	#电影图片的存放路径
	movie_img_path = scrapy.Field()

	#电影名
	movie_name = scrapy.Field()

	#电影类型
	movie_type = scrapy.Field()

	#电影图片URL
	movie_img_url = scrapy.Field()
