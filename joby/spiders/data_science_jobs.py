# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from joby.items import JobLoader, Job


class DataScienceJobsSpider(CrawlSpider):
    name = 'data-science-jobs'
    log = getLogger(name)
    parser_engine = 'lxml'

    allowed_domains = ['www.data-science-jobs.com']
    start_urls = ['http://www.data-science-jobs.com']
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse_job')
    pagination_links = Rule(LinkExtractor(allow='page=\d+'))
    rules = [job_links, pagination_links]

    def __init__(self, *args, **kwargs):
        super(DataScienceJobsSpider, self).__init__(*args, **kwargs)

        self.xbase = '//div[@id="detailView"]/'

        self.response = None
        self.loader = None
        self.soup = None

    def parse_job(self, response):
        self.response = response

        self.soup = BeautifulSoup(response.body, self.parser_engine)
        self.loader = JobLoader(item=Job(), response=response)

        self.parse_job_overview()
        self.parse_job_details()
        self.parse_company_info()
        self.parse_webpage_info()

        self.loader.load_item()
        self.log.info('Loaded job from %s', response.url)
        return self.loader.load_item()

    def parse_job_overview(self):
        table = self.soup.find('table', class_='detailViewTable')
        overview_fields = {
            'Category': 'job_category',
            'Type': 'contract_type',
            'Home Office': 'allows_remote',
            'Min. Budget': 'salary',
            'Age': 'days_since_posted',
            'Reference ID': 'reference_id',
            'Apply URL': 'apply_url',
            'Duration': 'duration',
            'Workload': 'workload',
            'Contact Person': 'contact_person',
            'Contact Phone': 'contact_phone',
        }
        self._parse_table(table, overview_fields)
        self.log.info('Parsed job overview from %s', self.response.url)

    def parse_job_details(self):
        self.loader.add_xpath('keywords', self.xbase + 'div[4]/div[2]/text()')
        self.loader.add_xpath('description', self.xbase + 'div[3]/div[2]/text()')
        self.loader.add_xpath('abstract', self.xbase + 'div[2]/div[2]/p/text()')
        self.log.info('Parsed job details from %s', self.response.url)

    def parse_company_info(self):
        table = self.soup.find_all(class_='detailViewTable')[1]
        company_fields = {
            'Name': 'company_name',
            'Description': 'company_description',
            'Website': 'company_url',
        }
        self._parse_table(table, company_fields)
        self.log.info('Parsed company details from %s', self.response.url)

    def parse_company_address(self):
        self.loader.add_xpath('company_address', self.xbase + 'div[6]/div[2]/table/tbody/tr/td[1]/address/text()')
        self.log.info('Parsed company address from %s', self.response.url)

    def parse_webpage_info(self):
        self.loader.add_xpath('job_title', self.xbase + 'h1/text()')
        self.loader.add_value('website_url', self.response.url)
        self.loader.add_value('job_url', self.response.url)
        self.loader.add_value('website_job_id', self.response.url)
        self.log.info('Parsed webpage info from %s', self.response.url)

    def _parse_table(self, table, expected_keys):
        self.log.info('Parsing table from %s', self.response.url)

        key_tags = table.find_all('td', class_='detailViewTableKey')
        value_tags = table.find_all('td', class_='detailViewTableValue')

        def extract(tag):
            if tag.next_element.name == 'a':
                return tag.next_element.attrs['href']
            else:
                return tag.text

        keys = map(extract, key_tags)
        values = map(extract, value_tags)
        rows = dict(zip(keys, values))
        unscraped = set(keys) - set(expected_keys.values())

        if unscraped:
            self.log.warning('Not scraping %s', list(unscraped))

        for label, key in expected_keys.items():
            if label in keys:
                self.loader.add_value(key, rows[label])
                self.log.debug('Scraped %s = %s', key, rows[label])
            else:
                self.log.debug('%s is missing', key)
