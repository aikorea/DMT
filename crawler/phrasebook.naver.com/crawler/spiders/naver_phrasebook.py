# -*- coding: utf-8 -*-
import scrapy


class NaverPhrasebookSpider(scrapy.Spider):
	name = "naver_phrasebook"
	allowed_domains = ["phrasebook.naver.com"]
	start_urls = (
		'http://phrasebook.naver.com/?targetLanguage=en/',
	)

	def parse(self, response):
		for href in response.xpath('//ul[@class="lst_sort2"]/li/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_level1)

	def parse_level1(self, response):
		for href in response.xpath('//dl[@class="lst_sort"]/dd/span/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_level2)

	def parse_level2(self, response):
		for href in response.xpath('//dl[@class="lst_sort sort_small"]/dd/span/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_level3)

	def parse_level3(self, response):
		for part in response.xpath('//div[@id="main_content"]/div/ul/li'):
			korean = part.xpath('span[@class="info_txt"]').extract_first()
			english = part.xpath('div/span[@class="info_txt2"]').extract_first()
			with open("output.txt", "ab") as f:
				f.write(self.remove_tag(korean.encode('UTF-8')) + '\n')
				f.write(self.remove_tag(english.encode('UTF-8')) + '\n')

	def remove_tag(self, str):
		ret = ""
		tag = 0
		for i in range(0, len(str)):
			if str[i] == '<':
				tag += 1
			if tag == 0:
				ret += str[i]
			if str[i] == '>':
				tag -= 1

		return ret.strip()
