""" Test the data_science_jobs spider. """


from os.path import join

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.http import HtmlResponse

from joby.spiders.data_science_jobs import DataScienceJobsSpider
from joby.items import Job, JobLoader
from joby.settings import TEST_ASSETS_DIR


def test_parse_overview_table_():
    with open(join(TEST_ASSETS_DIR, 'data_science_job.html')) as test_file:
        test_html = test_file.read()

    expected_fields = {
        'job_category': 'Data Scientist',
        'apply_url': 'https://mydis.dis-ag.com/kd_1/Registration.aspx?tID=1&lID=0{0}',
        'days_since_posted': '453 days',
        'contract_type': 'Employee',
        'workload': 'full-time',
        'allows_remote': 'negotiable',
        'duration': 'unlimited',
    }

    dummy_url = 'http://dummy.com'

    spider = DataScienceJobsSpider()
    spider.response = HtmlResponse(dummy_url, body=test_html, request=Request(url=dummy_url), encoding='utf-8')
    spider.loader = JobLoader(item=Job(), response=spider.response)
    spider.soup = BeautifulSoup(spider.response.body, spider.parser_engine)
    spider.parse_job_overview()
    spider.loader.load_item()

    assert dict(spider.loader.item) == expected_fields
