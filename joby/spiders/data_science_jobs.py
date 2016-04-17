# -*- coding: utf-8 -*-
import scrapy


class DataScienceJobsSpider(scrapy.Spider):
    name = "data-science-jobs"
    allowed_domains = ["www.data-science-jobs.com"]
    start_urls = (
        'http://www.data-science-jobs.com/',
    )

    def parse(self, response):
        pass
