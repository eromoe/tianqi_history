#!/usr/bin/python
#-*-coding:utf-8-*-


# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import re

def extract_int(s):
    if isinstance(s,unicode):
        return int(re.sub(r'[^\d-]+', '', s.encode('utf-8')))
    else:
        return int(re.sub(r'[^\d-]+', '', s))


class WeatherItem(Item):
    # url = Field()
    purl = Field()
    zone_id = Field()
    weather = Field()
    wind_direction = Field()
    wind_power = Field()
    max_t = Field()
    min_t = Field()
    date =  Field()


