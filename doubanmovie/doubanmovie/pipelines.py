# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from doubanmovie.items import *
import pymysql.cursors

class PopularMovieSQLPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                        user = 'douban',
                                        password = '12306',
                                        db = 'doubanmovie',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT popularmovie(id, film_title, director,actor,region,release_date," \
                   "film_types,grade,intro,poster,yyyy,turn) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s,%s)"

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item["movie_id"], item["movie_name"], item["movie_director"],
                item["movie_performer"], item["movie_region"], item["movie_release_date"], item["movie_type"],
                item["movie_score"],item["movie_intro"],item["movie_img_url"],item["movie_year"],item["turn"]))
        self.conn.commit()


class NewMovieSQLPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                        user = 'douban',
                                        password = '12306',
                                        db = 'doubanmovie',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO newmovie(id,film_title, director,actor,region,release_date," \
                   "film_types,grade,intro,poster,yyyy,turn) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s , %s,%s,%s)"

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item["movie_id"],item["movie_name"], item["movie_director"],
                item["movie_performer"], item["movie_region"], item["movie_release_date"], item["movie_type"],
                item["movie_score"] , item["movie_intro"],item["movie_img_url"] ,  item["movie_year"],item["turn"]))
        self.conn.commit()

class UpComingSQLPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                        user = 'douban',
                                        password = '12306',
                                        db = 'doubanmovie',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO upcoming(id,film_title, director,actor,region,release_date," \
                   "film_types,intro,poster,yyyy,turn) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item["movie_id"],item["movie_name"], item["movie_director"],
                item["movie_performer"], item["movie_region"], item["movie_release_date"], item["movie_type"],
                item["movie_intro"],item["movie_img_url"] , item["movie_year"],item["turn"]))
        self.conn.commit()

class NowPlayingSQLPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                        user = 'douban',
                                        password = '12306',
                                        db = 'doubanmovie',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO nowplaying(id ,film_title, director,actor,region," \
                   "release_date,film_types,grade,intro,poster,yyyy,city,turn) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item["movie_id"],item["movie_name"],item["movie_director"],
                item["movie_performer"],item["movie_region"],item["movie_release_date"],item["movie_type"],
                item["movie_score"],item["movie_intro"],item["movie_img_url"],item["movie_year"],item["city"],item["turn"]))
        self.conn.commit()
