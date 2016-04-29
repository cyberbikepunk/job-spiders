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
            'job_category': 'Category',
            'contract_type': 'Type',
            'allows_remote': 'Home Office',
            'salary': 'Min. Budget',
            'days_since_posted': 'Age',
            'reference_id': "Reference ID",
            'apply_url': 'Apply URL',
            'duration': 'Duration',
            'workload': 'Workload',
            'contact_person': "Contact Person",
            'contact_phone': 'Contact Phone',
        }

        self._parse_table(table, overview_fields)
        self.log.info('Parsed company details from %s', self.response.url)

    def parse_job_details(self):
        self.loader.add_xpath('keywords', self.xbase + 'div[4]/div[2]/text()')
        self.loader.add_xpath('description', self.xbase + 'div[3]/div[2]/text()')
        self.loader.add_xpath('abstract', self.xbase + 'div[2]/div[2]/p/text()')
        self.log.info('Parsed job details from %s', self.response.url)

    def parse_company_info(self):
        table = self.soup.find_all(class_='detailViewTable')[1]
        company_fields = {
            'company_name': 'Name',
            'company_description': 'Description',
            'company_url': 'Website',
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
        self.log.info('Parsing the job overview table from %s', self.response.url)

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

        for key, item_label in expected_keys.items():
            if item_label in keys:
                self.loader.add_value(key, rows[item_label])
                self.log.debug('Scraped %s = %s', key, rows[item_label])
            else:
                self.log.debug('%s is missing', key)
