# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class DataScienceJobsSpider(CrawlSpider):
    log = getLogger(__name__)
    name = 'data-science-jobs'
    allowed_domains = ['www.data-science-jobs.com', 'fonts.googleapis.com', 'jobs.lever.com']
    start_urls = ['http://www.data-science-jobs.com/']
    test = Rule(LinkExtractor(allow='family'), callback='parse')
    test2 = Rule(LinkExtractor(allow='comtravo'), callback='parse')
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse')
    pagination_links = Rule(LinkExtractor(allow='\?page=\d+'), callback='parse')
    rules = [job_links, pagination_links, test, test2]
    response = None

    def parse(self, response):
        self.log.info('Parsing %s', response.url)
