# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

import pymysql.cursors

project_path = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, project_path)

# import the spiders you want to run
from spiders.NewMovie import NewMovieSpider
from spiders.NowPlaying import NowPlayingSpider
from spiders.PopularMovie import PopularMovieSpider
from spiders.UpComing import UpComingSpider

# scrapy api imports
from twisted.internet import reactor,defer
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)

def sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d

@defer.inlineCallbacks
def crawl():
    conn = pymysql.connect(host='localhost', port=3306,
                                user='douban',
                                password='12306',
                                db='doubanmovie',
                                charset='utf8')

    UpComingSpider_count = 5
    PopularMovieSpider_count = 1
    NowPlayingSpider_count = 5
    NewMovieSpider_count = 1
    first = True

    last_turn = -1
    while True:
        n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s = time.time()
        turn = int(s / 86400)

        if turn == last_turn:
            sleep(5)
            continue

        print "new turn", turn, n
        last_turn = turn

        with conn.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO turns VALUES (%s, %s)", (turn, n))
        conn.commit()

        if first or turn % NewMovieSpider_count == 0:
            yield crawler.crawl(NewMovieSpider,turn)
        if first or turn % PopularMovieSpider_count == 0:
            yield crawler.crawl(PopularMovieSpider,turn)
        if first or turn % UpComingSpider_count == 0:
            yield crawler.crawl(UpComingSpider,turn)
        if first or turn % NowPlayingSpider_count == 0:
            yield crawler.crawl(NowPlayingSpider,turn)

        first = False
        e = time.time()
        left = int(86400 - e + s)

        if left > 0:
            print "sleep", left
            sleep(left)

    print "crawler over"

crawl()
crawler.start()