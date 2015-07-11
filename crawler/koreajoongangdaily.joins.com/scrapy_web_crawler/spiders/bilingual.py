# -*- coding: utf-8 -*-
import scrapy
import urlparse

class BilingualSpider(scrapy.Spider):
	name = "bilingual"
	allowed_domains = ["koreajoongangdaily.joins.com"]
	start_urls = (
		'http://koreajoongangdaily.joins.com/news/list/list.aspx?gCat=060201',
	)

	def parse(self, response):
		pg_arr = response.xpath('//div[@id="paginate"]/a[@class="pg"]/text()').extract()
		last_page = int(pg_arr[-1].encode('UTF-8'))
		for i in range(1, last_page + 1):
			# url = response.urljoin(response.url + "&pgi=" + str(i))
			url = response.url + "&pgi=" + str(i)
			yield scrapy.Request(url, callback=self.parse_page)

	def parse_page(self, response):
		news_arr = response.xpath('//a[@class="title_cr"]/@href').extract()
		for url in news_arr:
			news_url = response.urljoin(url);
			yield scrapy.Request(news_url, callback=self.parse_news)

	def parse_news(self, response):
		parsed = urlparse.urlparse(response.url)
		aids = urlparse.parse_qs(parsed.query)['aid']
		if len(aids) == 0:
			raise Exception('aid not found')

		aid = aids[0]
		filename_html = 'html/' + aid + '.html'
		with open(filename_html, 'w') as f:
			body_text = response.body
			f.write(body_text)
		pass

	def log(self, str):
		with open('debug.log', 'ab') as debug:
			debug.write(str + "\n")
