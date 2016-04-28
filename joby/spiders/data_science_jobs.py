# -*- coding: utf-8 -*-

from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from joby.items import DataScienceJobsLoader, JobItem


class DataScienceJobsSpider(CrawlSpider):
    name = 'data-science-jobs'
    log = getLogger(name)

    allowed_domains = ['www.data-science-jobs.com']
    start_urls = ['http://www.data-science-jobs.com']
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse_job')
    pagination_links = Rule(LinkExtractor(allow='page=\d+'))
    rules = [job_links, pagination_links]

    def __init__(self, *args, **kwargs):
        super(DataScienceJobsSpider, self).__init__(*args, **kwargs)
        self.response = None
        self.loader = None

    def parse_job_overview_table(self):
        soup = BeautifulSoup(self.response.body, 'lxml')
        self.log.debug('Parsing id=detailViewTable from %s', self.response.url)

        table = soup.find('table', class_='detailViewTable')
        fields_found = map(lambda x: x.text, table.find_all('td', class_='detailViewTableKey'))
        values_found = map(lambda x: x.text, table.find_all('td', class_='detailViewTableValue'))

        rows = dict(zip(fields_found, values_found))
        fields_expected = {
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

        unscraped_fields = set(fields_found) - set(fields_expected.values())
        if unscraped_fields:
            self.log.warning('%s fields are not being scraped', list(unscraped_fields))

        for item_name, item_label in fields_expected.items():
            if item_label in fields_found:
                self.loader.add_value(item_name, rows[item_label])
                self.log.debug('Scraped %s = %s', item_name, rows[item_label])
            else:
                self.log.debug('%s field is missing', item_name)

    def parse_job(self, response):
        self.response = response
        self.loader = DataScienceJobsLoader(item=JobItem(), response=response)
        self.parse_job_overview_table()
        self.parse_job_description_boxes()
        self.loader.load_item()

        self.log.info('Loaded job from %s', response.url)

        return self.loader.load_item()

    def parse_job_description_boxes(self):
        pass
