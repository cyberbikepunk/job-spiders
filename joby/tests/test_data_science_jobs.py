""" Test the data_science_jobs spider. """


from joby.spiders.data_science_jobs import DataScienceJobsSpider
from joby.items import JobLoader, Job
from joby.tests.utilities import make_offline_parser
from datetime import date


TEST_URL = 'http://www.data-science-jobs.com/detail/20'


# noinspection PyShadowingNames
def test_parse_overview_table():
    expected_fields = {
        'job_category': u'Data Scientist',
        'apply_url': u'https://mydis.dis-ag.com/kd_1/Registration.aspx?tID=1&lID=0{0}',
        'publication_date': str(date.today() - date(2015, 2, 2)).split(',')[0],
        'days_since_posted': str(date.today() - date(2015, 2, 2)).split(',')[0],
        'contract_type': u'Employee',
        'workload': u'full-time',
        'allows_remote': u'negotiable',
        'duration': u'unlimited',
    }
    parser = make_offline_parser(DataScienceJobsSpider,
                                 'data_science_jobs',
                                 'DataScienceJobsParser',
                                 TEST_URL,
                                 ('job', Job, JobLoader))

    parser.parse_job_overview()
    parser.job.load_item()

    assert dict(parser.job.item) == expected_fields
