#*- coding: utf-8 -*-
import scrapy
from scrapy import log, Spider, Item, Field

from urlparse import urlparse, parse_qs
import json
import time
import os
import urllib
import chardet
import re
import codecs
import threading
from bs4 import BeautifulSoup

GOM_DOMAIN = "http://gom.gomtv.com/"
SUB_LIST_URL = "http://gom.gomtv.com/main/index.html?ch=subtitles&pt=l&menu=subtitles&lang=3&page=%s"
SUB_LIST_START_PAGE = 1
SUB_LIST_END_PAGE = 1
SUB_DOWN_URL = "http://gom.gomtv.com/main/index.html/%s?ch=subtitles&pt=down&intSeq=%s&capSeq=%s"
DOWN_SUB_DIR = 'subtitle'

class DownItem(Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class GomSpider(Spider):
    name = "gom"
    allowed_domains = [
        "gom.gomtv.com",
    ]

    #custom_settings = {'CONCURRENT_REQUESTS':5}

    def __init__(self, page=None):
        if page is not None:
            SUB_LIST_START_PAGE, SUB_LIST_END_PAGE = [int(temp) for temp in page.split('-')]
        self.start_urls = [SUB_LIST_URL % (i+1) for i in range(SUB_LIST_START_PAGE, SUB_LIST_END_PAGE + 1)]
        if not os.path.exists(DOWN_SUB_DIR):
            os.mkdir(DOWN_SUB_DIR)

    def parse(self, response):
        # Select subtitle article page URL
        for row in response.xpath("//table[@class='tbl_lst']/tbody/tr"):
            if row.xpath("./td[1]/*").extract_first().startswith('<span'):
                page1_url = response.urljoin(row.xpath("./td[3]/a/@href").extract_first())
                yield scrapy.Request(page1_url, callback=self.parse_page1)

    def parse_page1(self, response):
        onclick_str = response.xpath(".//a[@class='btn_type3 download']/@onclick").extract_first()
        temp = onclick_str.split("'")
        intSeq, capSeq, fileName = [int(temp[1]), int(temp[3]), temp[5]]
        fileName = fileName.replace(' ', '_')
        down_url = SUB_DOWN_URL % (fileName, intSeq, capSeq)
        yield scrapy.Request(down_url, callback=self.save_subtitle)

    def save_subtitle(self, response):
        temp = urlparse(response.url)
        query_dict = parse_qs(temp.query)

        smi_filename = temp.path[temp.path.rfind('/')+1:]
        if smi_filename.endswith('.smi'):
            smi_filename = query_dict['intSeq'][0] + '_' + query_dict['capSeq'][0] + '_' + urllib.unquote(smi_filename).decode('utf-8')
            smi_filepath = os.path.join(DOWN_SUB_DIR, smi_filename)
            if not os.path.exists(smi_filepath):
                with open(smi_filepath, "wb") as f:
                    f.write(response.body)
