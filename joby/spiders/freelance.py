# -*- coding: utf-8 -*-

from logging import getLogger
from requests import post
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class FreelanceSpider(CrawlSpider):
    log = getLogger(__name__)
    name = 'freelance'
    allowed_domains = ['www.freelance.de']
    start_urls = ['http://www.freelance.de']
    job_links = Rule(LinkExtractor(allow='\/Freiberufler\/\d+'), callback='parse')
    pagination_links = Rule(LinkExtractor(allow='\/Freiberufler\/K\/IT-Entwicklung-Freiberufler\/\d+-\d+'))
    rules = [job_links, pagination_links]

    def __init__(self, *args, **kwargs):
        super(FreelanceSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.log.info('Parsing %s', response.url)
