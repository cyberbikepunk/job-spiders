# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from joby.items import DataScienceJobsLoader, DataScienceJob


class DataScienceJobsSpider(CrawlSpider):
    name = 'data-science-jobs'
    allowed_domains = ['www.data-science-jobs.com']
    start_urls = ['http://www.data-science-jobs.com']
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse_job')
    pagination_links = Rule(LinkExtractor(allow='page=\d+'))
    rules = [job_links, pagination_links]

    def __init__(self, *args, **kwargs):
        super(DataScienceJobsSpider, self).__init__(*args, **kwargs)

        self.log = getLogger(__name__)
        self.response = None
        self.loader = None

    def parse_job_overview_table(self):
        soup = BeautifulSoup(self.response.text)

        table = soup.find('table', class_='detailViewTable')
        keys = table.find_all('td', class_='detailViewTableKey')
        values = table.find_all('td', class_='detailViewTableValue')

        rows = dict(zip(keys, values))

        self.loader.add_item('category', rows['Category'])
        self.loader.add_item('job_category', rows['Type'])
        self.loader.add_item('allows_remote', rows['Home_Office'])
        self.loader.add_item('salary', rows['Min. Budget'])
        self.loader.add_item('days_since_posted', rows['Age'])
        self.loader.add_item('job_id', rows['Reference ID'])

        self.log.debug('Scraped %s', rows)

    def parse_job(self, response):
        self.response = response
        self.loader = DataScienceJobsLoader(item=DataScienceJob(), response=response)
        self.parse_job_overview_table()
        self.parse_job_description_boxes()
        self.loader.load_item()

        self.log.info('Loaded %s from %s', self.loader, response.url)

        return self.loader

    def parse_job_description_boxes(self):
        pass
