#*- coding: utf-8 -*-
import scrapy
from scrapy import log, Spider, Item, Field

from urlparse import urlparse, parse_qs
import json
import time

LEC_LIST_URL = "http://www.ted.com/talks?language=ko&page=%s"
LEC_LIST_MAX = 54
LEC_URL = "http://www.ted.com/talks/%s?language=ko"
SCRIPT_EN_URL = "http://www.ted.com/talks/%s/transcript?language=en"
SCRIPT_KO_URL = "http://www.ted.com/talks/%s/transcript?language=ko"
SCRIPT_EN_PATH = "scripts/%s-en.json"
SCRIPT_KO_PATH = "scripts/%s-ko.json"

class TedSpider(Spider):
    name = "ted"
    allowed_domains = [
        "www.ted.com",
    ]
    #start_urls = []

    # If CONCURRENT_REQUESTS is greater than 2, requests will receive HTTP 429 response
    custom_settings = {'CONCURRENT_REQUESTS':1} 

    def __init__(self):
        self.start_urls = [LEC_LIST_URL % (i+1) for i in range(LEC_LIST_MAX)]
        #self.start_urls = [DIC_URL % 100000]

    def parse(self, response):
        # Select lecture names
        for href in response.xpath("//div[@class='media__image media__image--thumb talk-link__image']/a/@href").extract():
            lec_name = href.replace("?", "/").split("/")[2]
            en_script_url = SCRIPT_EN_URL % lec_name
            ko_script_url = SCRIPT_KO_URL % lec_name
            yield scrapy.Request(en_script_url, callback=self.parse_en_script)
            yield scrapy.Request(ko_script_url, callback=self.parse_ko_script)

    def parse_en_script(self, response):
        lec_name = response.xpath("//select[@class='form-control form-control--dropdown talk-transcript__language m3']/@data-slug").extract_first()
        
        script = []
        for span in response.xpath("//span[@class='talk-transcript__fragment']"):
            data_time = span.xpath("./@data-time").extract_first()
            en = span.xpath("./text()").extract_first().replace("\n", " ")
            script.append({'data_time':data_time, 'en':en})

        script_path = SCRIPT_EN_PATH % lec_name
        with open(script_path, "w") as fd:
            json.dump(script, fd, indent=2)


    def parse_ko_script(self, response):
        lec_name = response.xpath("//select[@class='form-control form-control--dropdown talk-transcript__language m3']/@data-slug").extract_first()
        
        script = []
        for span in response.xpath("//span[@class='talk-transcript__fragment']"):
            data_time = span.xpath("./@data-time").extract_first()
            ko = span.xpath("./text()").extract_first().replace("\n", " ")
            script.append({'data_time':data_time, 'ko':ko})

        script_path = SCRIPT_KO_PATH % lec_name
        with open(script_path, "w") as fd:
            json.dump(script, fd, indent=2)
