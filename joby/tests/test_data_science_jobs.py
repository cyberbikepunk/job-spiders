""" Test the data_science_jobs spider. """


from joby.items import JobLoader, Job
from joby.tests.utilities import make_offline_parser
from datetime import date


TEST_URL = 'http://www.data-science-jobs.com/detail/20'


# noinspection PyShadowingNames
def test_parse_overview_table():
    expected_fields = {
        'job_category': 'Data Scientist',
        'apply_url': 'https://mydis.dis-ag.com/kd_1/Registration.aspx?tID=1&lID=0{0}',
        'publication_date': date(2015, 2, 3),
        'contract_type': 'Employee',
        'workload': 'full-time',
        'allows_remote': 'negotiable',
        'duration': 'unlimited',
    }
    parser = make_offline_parser('data_science_jobs', 'DataScienceJobsJobParser', TEST_URL, ('job', Job, JobLoader))
    parser.parse_job_overview()
    parser.job.load_item()
    assert dict(parser.job.item) == expected_fields
