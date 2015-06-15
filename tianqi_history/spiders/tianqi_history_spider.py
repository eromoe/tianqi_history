#!/usr/bin/python
#-*-coding:utf-8-*-

import time, datetime
from pprint import pprint
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from tianqi_history.items import WeatherItem
from tianqi_history import settings
from tianqi_history.utils.select_result import strip_null,deduplication,clean_url
from scrapy import log
from datetime import datetime
# from dateutil.relativedelta import relativedelta

import re
import os
import pickle

take_first_strip_dash = lambda x: x[0].strip() if x and len(x) > 0 and isinstance(x[0], basestring) and x[0].strip('- ') else None

take_first_strip = lambda x: x[0].strip() if x and len(x) > 0 and isinstance(x[0], basestring) else None

take_first = lambda x: x[0] if x else None



URL_FILE_PATH = getattr(settings,'URL_FILE_PATH', 'urls')

ONLY_CITY_LEVEL = getattr(settings,'ONLY_CITY_LEVEL', True)

DATE_RANGE_START = getattr(settings,'DATE_RANGE_START', None)
DATE_RANGE_END = getattr(settings,'DATE_RANGE_END', None)

if DATE_RANGE_START:
	DATE_RANGE_START = datetime.strptime(DATE_RANGE_START,'%Y%m')

if DATE_RANGE_END:
	DATE_RANGE_END = datetime.strptime(DATE_RANGE_END,'%Y%m')
else:
	DATE_RANGE_END = datetime.now()

if DATE_RANGE_START and DATE_RANGE_START > DATE_RANGE_END:
	raise Exception('DATE_RANGE_START > DATE_RANGE_END not allow !!!!')


print URL_FILE_PATH
ERROR_FILE_PATH = 'error.txt'

def read_urls():
	global URL_FILE_PATH
	urls = None
	if os.path.exists(URL_FILE_PATH):
		try:
			with open(URL_FILE_PATH, 'rb') as f:
				data = f.read()
				urls = pickle.loads(data)
		except:
				pass

	return urls


def write_urls(urls):
	global URL_FILE_PATH
	with open(URL_FILE_PATH, 'wb') as f:
		f.write(pickle.dumps(urls))


def log_error(url):
	global ERROR_FILE_PATH
	with open(URL_FILE_PATH, 'ab') as f:
		f.write(url+'\n')


from lxml import etree,html
import requests

def get_html(url):
	r = requests.get(url,timeout = 20)
	return html.document_fromstring(r.content)


def get_urls():

	urls = read_urls()

	if urls is None:
		h = get_html('http://lishi.tianqi.com/')
		urls = h.xpath('//div[@id="tool_site"]/div[2]/ul/li/a/@href')
		urls = [str(u) for u in urls if u !='#' ]
		write_urls(urls)

	return urls


class WeatherSpider(Spider):
	name = "weather"
	start_urls = get_urls()


	def get_zone_id(self, response):
		zone_id, name = self.get_zone_id_and_name(response)

		return zone_id

	def get_zone_id_and_name(self, response):
		sel = Selector(response)

		l_selected = take_first(sel.xpath('//select[@id="zone"]/option[@selected]'))

		zone_id = take_first_strip(l_selected.xpath('@value').extract())

		name = take_first_strip(l_selected.xpath('text()').extract())[2:]

		if not zone_id:
			raise Exception('url: %s do not have zone_id' % response.url)

		return zone_id, name


	def check_target_response(self, response):
		if ONLY_CITY_LEVEL:
			zone_id = self.get_zone_id(response)

			# self.log('zone_id: %s,  endswith:%s' % (zone_id, zone_id.endswith('01')))
			#  一般一级市  or   北京、天津、上海、重庆
			if zone_id.endswith('01') or zone_id.endswith('0100'):
				return True
			else:
				return False
		else:
			return True

	def filter_by_date_range(self, month_links):
		for m in month_links:
			date_str = m.split('/')[-1].split('.')[0]
			md = datetime.strptime(date_str, '%Y%m')
			if DATE_RANGE_START:
				if md < DATE_RANGE_START:
					continue

			if DATE_RANGE_END:
				if md > DATE_RANGE_END:
					continue

			# log.msg("m:%s " % m, level=log.INFO, spider=self)

			yield m

	def parse(self, response):
		# test
		# return self.parse_detail(response)
		if self.check_target_response(response):
			sel = Selector(response)
			month_links = sel.xpath(u'//div[@class="tqtongji1"]//a/@href').extract()
			filtered_month_links = self.filter_by_date_range(month_links)
			for month_link in filtered_month_links:
				self.log('month_link: %s' % month_link)
				month_link = clean_url(response.url, month_link, response.encoding)
				yield Request(url=month_link, callback=self.parse_detail)


	def parse_detail(self, response):
		sel = Selector(response)

		zone_id, name = self.get_zone_id_and_name(response)

		w_list = sel.xpath(u'//div[@class="tqtongji2"]/ul')[1:]
		items = []
		for w in w_list:
			item = WeatherItem()

			item['zone_id'] = zone_id
			try:
				date = take_first_strip(w.xpath('li[1]/a/text()').extract())

				url = take_first_strip(w.xpath('li[1]/a/@href').extract())

				if date:
					date = datetime.strptime(date,'%Y-%m-%d')
				else:
					if url:
						url_date_text = url.split('/')[-1].split('.')[0]
						date = datetime.strptime(url_date_text,'%Y%m%d')
			except Exception as e:
				self.log("url:%s error" % e, level=log.ERROR)



			item['purl'] = response.url
			item['name'] = name
			# item['url'] = url
			item['date'] = date
			item['max_t'] = take_first_strip(w.xpath('li[2]/text()').extract())
			item['min_t'] = take_first_strip(w.xpath('li[3]/text()').extract())
			item['weather'] = take_first_strip(w.xpath('li[4]/text()').extract())
			item['wind_direction'] = take_first_strip(w.xpath('li[5]/text()').extract())
			item['wind_power'] = take_first_strip(w.xpath('li[6]/text()').extract())

				
			items.append(item)

		self.log("parse zone_id: %s , w_list_count:%s ,items_count:%s, purl:%s" % (zone_id, len(w_list), len(items), response.url), level=log.DEBUG)
		if len(w_list) != len(items):
			self.log("w_list_count:%s  not equel to items_count:%s" % (len(w_list), len(items)), level=log.ERROR)

		for item in items:
			yield item

			# return items
