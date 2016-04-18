# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class DataScienceJobsSpider(CrawlSpider):
    log = getLogger(__name__)
    name = 'data-science-jobs'
    allowed_domains = ['www.data-science-jobs.com']
    start_urls = ['http://www.data-science-jobs.com']
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse_job')
    pagination_links = Rule(LinkExtractor(allow='page=\d+'))
    rules = [job_links, pagination_links]

    def parse_job(self, response):
        self.log.info('Parsing %s', response.url)


