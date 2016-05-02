"""" A crawler for the data-science-jobs.com website. """


from logging import getLogger
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from joby.items import JobLoader, Job
from joby.utilities import Parser


log = getLogger(__name__)


class DataScienceJobsSpider(CrawlSpider):
    name = 'data-science-jobs'
    allowed_domains = ['www.data-science-jobs.com']
    start_urls = ['http://www.data-science-jobs.com']
    job_links = Rule(LinkExtractor(allow='detail\/'), callback='parse_job')
    pagination_links = Rule(LinkExtractor(allow='page=\d+'))

    rules = [job_links, pagination_links]

    # noinspection PyUnresolvedReferences
    def parse_job(self, response):
        """ Parses all Job item fields.

        @url        http://www.data-science-jobs.com/detail/20
        @returns    items 1 16
        @returns    requests 0 0

        @scrapes    website_url website_job_id job_url job_title
        @scrapes    keywords description abstract
        @scrapes    company_name company_address company_description company_url
        @scrapes    publication_date

        """
        loader = JobLoader(item=Job(), response=response)
        parser = DataScienceJobsJobParser(response, job=loader)

        parser.parse_job_overview()
        parser.parse_job_details()
        parser.parse_company_info()
        parser.parse_company_address()
        parser.parse_webpage_info()

        parser.job.load_item()
        log.info('%s spider scraped %s', self.name, response.url)
        return parser.job.item


# noinspection PyUnresolvedReferences
class DataScienceJobsJobParser(Parser):
    X_BASE = '//div[@id="detailView"]/'
    X_TTILE = X_BASE + '/h1/text()'
    X_KEYWORDS = X_BASE + 'div[4]/div[2]/text()'
    X_ABSTRACT = X_BASE + 'div[2]/div[2]/p/text()'
    X_DESCRIPTION = X_BASE + 'div[3]/div[2]/text()'
    X_COMPANY_ADDRESS = X_BASE + 'div[6]/div[2]/table/tbody/tr/td[1]/address/text()'

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
        log.info('Parsed job overview from %s', self.response.url)

    def parse_job_details(self):
        self.job.add_xpath('keywords', self.X_KEYWORDS)
        self.job.add_xpath('description', self.X_DESCRIPTION)
        self.job.add_xpath('abstract', self.X_ABSTRACT)
        log.info('Parsed job details from %s', self.response.url)

    def parse_company_info(self):
        table = self.soup.find_all(class_='detailViewTable')[1]
        company_fields = {
            'Name': 'company_name',
            'Description': 'company_description',
            'Website': 'company_url',
        }
        self._parse_table(table, company_fields)
        log.info('Parsed company details from %s', self.response.url)

    def parse_company_address(self):
        self.job.add_xpath('company_address', self.X_COMPANY_ADDRESS)
        log.info('Parsed company address from %s', self.response.url)

    def parse_webpage_info(self):
        self.job.add_xpath('job_title', self.X_TTILE)
        self.job.add_value('website_url', self.response.url)
        self.job.add_value('job_url', self.response.url)
        self.job.add_value('website_job_id', self.response.url)
        log.info('Parsed webpage info from %s', self.response.url)

    def _parse_table(self, table, expected_keys):
        log.info('Parsing table from %s', self.response.url)

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
            log.warning('Not scraping %s', list(unscraped))

        for label, key in expected_keys.items():
            if label in keys:
                self.job.add_value(key, rows[label])
                log.debug('Scraped %s = %s', key, rows[label])
            else:
                log.debug('%s is missing', key)
