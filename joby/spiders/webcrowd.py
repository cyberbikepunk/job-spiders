# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Spider


class WebcrowdSpider(Spider):
    log = getLogger(__name__)
    name = 'webcrowd'
    allowed_domains = ['www.webcrowd.net']
    start_urls = ['http://webcrowd.net/jobs/']

    def parse(self, response):
        self.log.info('Parsing %s', response.url)
