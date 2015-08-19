#!/usr/bin/python
#-*-coding:utf-8-*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from datetime import datetime,date
from twisted.internet.threads import deferToThread
from scrapy.utils.serialize import ScrapyJSONEncoder

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
import os

from models import Weather
from scrapy import signals


class JsonWriterPipeline(object):

    def __init__(self):
        self.counter = 0
        self.limit = 2000
        self.dir = './json'
        self.file = None
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.switch_json()

    def switch_json(self):
        # format  padding 用法
        # >>> '{:<30}'.format('left aligned')
        # 'left aligned                  '
        # >>> '{:>30}'.format('right aligned')
        # '                 right aligned'
        # >>> '{:^30}'.format('centered')
        # '           centered           '
        # >>> '{:*^30}'.format('centered')  # use '*' as a fill char
        # '***********centered***********'

        self.file_name = 'items-{0:0>2}.json'.format(self.counter/self.limit)
        if self.file:
            self.file.close()
        self.file = open(os.path.join(self.dir, self.file_name), 'ab')

    def process_item(self, item, spider):
        if self.counter % self.limit == 0:
            self.switch_json()
        line = json.dumps(dict(item)) + "\r\n"
        self.file.write(line)
        return item




DATE_ERROR_FILE_PATH = 'date_error.txt'


def log_date_error(url):
  global DATE_ERROR_FILE_PATH
  with open(DATE_ERROR_FILE_PATH, 'ab') as f:
    f.write(url+'\n')


class SQLitePipline(object):
    DBPATH = 'weather.db'

    def __init__(self):

        self.item_count = 0
        self.bulk_limit = 500
        self.spider_stoped = False

        try:
            engine = getattr(self, 'engine', None)
            if engine is None:
                self.engine = create_engine('sqlite:///%s' % self.DBPATH)
                self.Session = sessionmaker(bind=self.engine)
                self.session = self.Session()
        except Exception as e:
            print "ERROR(SQLite): %s"%(str(e),)


    @classmethod
    def from_crawler(cls, crawler):
        cls.DBPATH = crawler.settings.get('SQLite_DBPATH', SQLitePipline.DBPATH)
        pipe = cls()
        pipe.crawler = crawler

        crawler.signals.connect(cls.handle_engine_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(cls.handle_spider_closed, signal=signals.spider_closed)

        return pipe

    def finish_job(self):
        self.spider_stoped = True
        self.session.commit()

    def handle_spider_closed(self, spider, reason):
        self.finish_job()

    def handle_engine_stopped(self):
        self.finish_job()

    def process_item(self, item, spider):
        try:
            date = item.get('date')

            if not date:
                log_date_error(item.get('purl'))

            w = Weather(
                name=item.get('name'),
                zone_id=item.get('zone_id'),
                weather=item.get('weather'),
                wind_direction=item.get('wind_direction'),
                wind_power=item.get('wind_power'),
                max_t=item.get('max_t'),
                min_t=item.get('min_t'),
                date=date,

            )
            self.session.add(w)

            self.item_count +=1

            if self.spider_stoped or (self.item_count % self.bulk_limit == 0):
                self.session.commit()

        except IntegrityError as e:
            log.msg("database error, item%s, detail:%s" % (item, e) ,level=log.ERROR, spider=spider)

            self.session.rollback()


        return item
