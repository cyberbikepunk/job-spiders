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
        """ Returns a Job item.

        @url        http://www.data-science-jobs.com/detail/20
        @returns    items 1
        @returns    requests 0

        parse_overview_table
        --------------------
        @scrapes reference_id
        @scrapes apply_url
        @scrapes job_category
        @scrapes contract_type
        @scrapes allows_remote
        @scrapes workload duration
        @scrapes publication_date
        @scrapes days_since_posted

        parse_webpage_info
        ------------------
        @scrapes website_url
        @scrapes website_job_id
        @scrapes job_url

        parse_job_details
        -----------------
        @scrapes job_title
        @scrapes keywords
        @scrapes description
        @scrapes abstract

        parse_company_info
        ------------------
        @scrapes company_name
        @scrapes company_description
        @scrapes company_url

        parse_company_address
        ---------------------
        @scrapes company_address
        @scrapes company_zipcode
        @scrapes company_country
        @scrapes company_city

        """
        loader = JobLoader(item=Job(), response=response)
        parser = DataScienceJobsParser(self, response, job=loader)

        parser.parse_job_overview()
        parser.parse_job_details()
        parser.parse_company_info()
        parser.parse_company_address()
        parser.parse_webpage_info()

        parser.job.load_item()
        log.info('%s spider scraped %s', self.name, response.url)
        return parser.job.item


# noinspection PyUnresolvedReferences
class DataScienceJobsParser(Parser):
    X_BASE = '//div[@id="detailView"]/'
    X_TTILE = X_BASE + '/h1/text()'
    X_KEYWORDS = X_BASE + 'div[4]/div[2]/text()'
    X_ABSTRACT = X_BASE + 'div[2]/div[2]/text()'
    X_DESCRIPTION = X_BASE + 'div[3]/div[2]/text()'
    CSS_COMPANY_ADDRESS = 'tr>td>address::text'

    def parse_job_overview(self):
        table = self.soup.find('table', class_='detailViewTable')
        overview_fields = (
            ('Category', 'job_category'),
            ('Type', 'contract_type'),
            ('Home Office', 'allows_remote'),
            ('Min. Budget', 'salary'),
            ('Age', 'days_since_posted'),
            ('Age', 'publication_date'),
            ('Reference ID', 'reference_id'),
            ('Apply URL', 'apply_url'),
            ('Duration', 'duration'),
            ('Workload', 'workload'),
            ('Contact Person', 'contact_person'),
        )
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
            ('Name', 'company_name'),
            ('Description', 'company_description'),
            ('Website', 'company_url'),
        }
        self._parse_table(table, company_fields)
        log.info('Parsed company details from %s', self.response.url)

    def parse_company_address(self):
        self.job.add_css('company_address', self.CSS_COMPANY_ADDRESS)
        self.job.add_css('company_city', self.CSS_COMPANY_ADDRESS)
        self.job.add_css('company_zipcode', self.CSS_COMPANY_ADDRESS)
        self.job.add_css('company_country', self.CSS_COMPANY_ADDRESS)
        log.info('Parsed company address from %s', self.response.url)

    def parse_webpage_info(self):
        self.job.add_xpath('job_title', self.X_TTILE)
        self.job.add_value('website_url', self.response.url)
        self.job.add_value('reference_id', self.response.url)
        self.job.add_value('job_url', self.response.url)
        self.job.add_value('website_job_id', self.response.url)
        log.info('Parsed webpage info from %s', self.response.url)

    def _parse_table(self, table, expected_pairs):
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

        expected_keys = [v for _, v in expected_pairs]
        unscraped = set(keys) - set(expected_keys)

        if unscraped:
            log.warning('Not scraping %s', list(unscraped))

        for label, key in expected_pairs:
            if label in keys:
                self.job.add_value(key, rows[label])
                log.debug('Scraped %s = %s', key, rows[label])
            else:
                log.debug('%s is missing', key)
