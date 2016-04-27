""" Test the data_science_jobs spider. """


from joby.items import DataScienceJobsLoader, DataScienceJob
from joby.spiders.data_science_jobs import DataScienceJobsSpider
from mock import Mock


def test_parse_overview_table_():
    html_table = """
        <html>
            <table class="detailViewTable">
                <tr>
                    <td class="detailViewTableKey">Category</td>
                    <td class="detailViewTableValue">Business Analyst</td>
                </tr>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Type</td>
                    <td class="detailViewTableValue">Employee</td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Workload</td>
                    <td class="detailViewTableValue">full-time</td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Duration</td>
                    <td class="detailViewTableValue">unlimited</td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Home Office</td>
                    <td class="detailViewTableValue">negotiable</td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Min. Budget</td>
                    <td class="detailViewTableValue">70000&nbsp;EUR</td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Contact E-Mail</td>
                    <td class="detailViewTableValue">
                        <a title="bla" href="javascript:_mailto('bla==','bla')" target="_blank">
                           <img src="/detail/247/contact" alt="Applicant contact" border="0">
                        </a>
                    </td></td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Contact Phone</td>
                    <td class="detailViewTableValue">08954459111</td></td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Reference ID</td>
                    <td class="detailViewTableValue">OZA282636</td></td>
                </tr>
                <tr>
                    <td class="detailViewTableKey">Age</td>
                    <td class="detailViewTableValue">178 days</td></td>
                </tr>
            </table>
        </html>
    """

    fields = {
        'job_category': 'Business Analyst',
        'contact_phone': '08954459111',
        'job_id': 'OZA282636',
        'days_since_posted': '178 days',
        'salary': '70000&nbsp;EUR',
        'job_type': 'Employee',
        'workload': 'full-time',
        'allows_remote': 'negotiable',
        'duration': 'unlimited',
    }

    spider = DataScienceJobsSpider()
    spider.response.text = html_table
    loader = DataScienceJobsLoader(item=DataScienceJob(), response=response)

    assert DataScienceJobsSpider().parse_job_overview_table() == fields
