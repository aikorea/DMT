#*- coding: utf-8 -*-

from scrapy import log, Spider, Item, Field

import re
import codecs
from urlparse import urlparse, parse_qs

DIC_URL = "http://m.endic.naver.com/example.nhn?sLn=kr&exampleId=%s&webCrawl=0"
DIC_MAX = 28544167
USER_URL = "http://m.endic.naver.com/example.nhn?sLn=kr&exampleId=%s&webCrawl=1"

class Sentence(Item):
    ko = Field() # korean
    en = Field() # english
    #qu = Field() # quality
    id = Field() # identification

class DicSpider(Spider):
    name = "dic"
    allowed_domains = [
        "m.endic.naver.com",
    ]
    #start_urls = []

    def __init__(self, idx=0, count=10000):
        idx, count = int(idx), int(count)
        self.start_urls = [DIC_URL % i for i in xrange(count*idx, count*(idx+1))]
        #self.start_urls = [DIC_URL % 100000]

    def parse(self, response):
        try:
            ko = response.xpath("//div[@class='cp_trans_area']/text()").extract()[0]
        except IndexError:
            log.msg("No sentence for %s" % response.url)
            return

        sentence = Sentence()
        sentence['ko'] = ko.encode('UTF-8')

        q = parse_qs(urlparse(response.url).query)
        sentence['id'] = int(q['exampleId'][0])

        h3 = response.xpath("//h3[@class='h_word saying']")
        text1 = h3.xpath("./text()").extract()[1:-1]
        text2 = h3.xpath("./span/a/text()").extract()
        result = [None]*(len(text1)+len(text2))
        result[::2] = text2
        result[1::2] = text1

        sentence['en'] = "".join(result).strip().encode('UTF-8')

        with open("output.txt", "ab+") as f:
            f.write(sentence['ko'] + '\n')
            f.write(sentence['en'] + '\n')

        yield sentence
