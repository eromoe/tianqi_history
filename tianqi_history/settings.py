# -*- coding: utf-8 -*-

# Scrapy settings for tianqi_history project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys


BOT_NAME = 'tianqi_history'

SPIDER_MODULES = ['tianqi_history.spiders']
NEWSPIDER_MODULE = 'tianqi_history.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianqi_history (+http://www.yourdomain.com)'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'lib')))


ITEM_PIPELINES = {
    # 'dmm.pipelines.RedisPipeline': 2,
    # 'tianqi_history.pipelines.JsonWriterPipeline': 1,
    'tianqi_history.pipelines.SQLitePipline': 10,
}


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 200,
}


RETRY_TIMES = 5

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 301, 302]


# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_DBNAME = "tianqi_history"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "123123"


LOG_ENABLED = True
LOG_FILE = "logs/weather.log"
LOG_LEVEL = 'INFO' 
LOG_STDOUT = True

ONLY_CITY_LEVEL = True

# from datetime import datetime

# 格式为 年月 %Y%m , 不填就当没有
DATE_RANGE_START = '201503'
DATE_RANGE_END = '201506'



SQLite_DBPATH = os.path.join(PROJECT_ROOT, 'weather.db')
URL_FILE_PATH = os.path.join(PROJECT_ROOT, 'urls.txt')

