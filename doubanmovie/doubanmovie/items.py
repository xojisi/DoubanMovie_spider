# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()

class PopularMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

	# 电影ID
	movie_id = scrapy.Field()
	#电影名
	movie_name = scrapy.Field()
	#电影演员
	movie_performer = scrapy.Field()
	#电影评分
	movie_score = scrapy.Field()
	#电影详细页面url
	movie_detail_url = scrapy.Field()
	#电影导演
	movie_director = scrapy.Field()
	#电影简介
	movie_intro = scrapy.Field()
	#电影制片国/地区
	movie_region = scrapy.Field()
	#电影类型
	movie_type = scrapy.Field()
	#电影图片URL
	movie_img_url = scrapy.Field()
	#电影上映时间
	movie_release_date = scrapy.Field()
	#电影年份
	movie_year = scrapy.Field()

	turn = scrapy.Field()

class NewMovieItem(scrapy.Item):
	# 电影ID
	movie_id = scrapy.Field()
	# 电影名
	movie_name = scrapy.Field()
	# 电影演员
	movie_performer = scrapy.Field()
	# 电影评分
	movie_score = scrapy.Field()
	# 电影详细页面url
	movie_detail_url = scrapy.Field()
	# 电影导演
	movie_director = scrapy.Field()
	# 电影简介
	movie_intro = scrapy.Field()
	# 电影制片国/地区
	movie_region = scrapy.Field()
	# 电影类型
	movie_type = scrapy.Field()
	# 电影图片URL
	movie_img_url = scrapy.Field()
	# 电影上映时间
	movie_release_date = scrapy.Field()
	# 电影年份
	movie_year = scrapy.Field()

	turn = scrapy.Field()


class UpComingItem(scrapy.Item):
	# 电影ID
	movie_id = scrapy.Field()
	# 电影名
	movie_name = scrapy.Field()
	# 电影演员
	movie_performer = scrapy.Field()
	# 电影详细页面url
	movie_detail_url = scrapy.Field()
	# 电影导演
	movie_director = scrapy.Field()
	# 电影简介
	movie_intro = scrapy.Field()
	# 电影制片国/地区
	movie_region = scrapy.Field()
	# 电影类型
	movie_type = scrapy.Field()
	# 电影图片URL
	movie_img_url = scrapy.Field()
	# 电影上映时间
	movie_release_date = scrapy.Field()
	# 电影年份
	movie_year = scrapy.Field()

	turn = scrapy.Field()

class NowPlayingItem(scrapy.Item):
	# 电影ID
	movie_id = scrapy.Field()
	# 电影名
	movie_name = scrapy.Field()
	# 电影演员
	movie_performer = scrapy.Field()
	# 电影评分
	movie_score = scrapy.Field()
	# 电影详细页面url
	movie_detail_url = scrapy.Field()
	# 电影导演
	movie_director = scrapy.Field()
	# 电影简介
	movie_intro = scrapy.Field()
	# 电影制片国/地区
	movie_region = scrapy.Field()
	# 电影类型
	movie_type = scrapy.Field()
	# 电影图片URL
	movie_img_url = scrapy.Field()
	# 电影上映时间
	movie_release_date = scrapy.Field()
	# 电影年份
	movie_year = scrapy.Field()
	# 电影上映城市
	city = scrapy.Field()

	turn = scrapy.Field()