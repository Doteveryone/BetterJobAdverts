import unittest
from jobcert import app
import os
from nose.tools import nottest

@nottest
def read_test_case(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(root_dir, '../jobcert', 'data', 'test-cases', filename)
    return file(test_file).read()

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_alive(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_about(self):
        rv = self.app.get('/about')
        assert rv.status == '200 OK'
        assert 'Better Job Adverts' in rv.data

    def test_league_tables(self):
        rv = self.app.get('/league-tables')
        assert rv.status == '200 OK'
        assert 'League table' in rv.data

    def test_salary(self):
        data = {'html': read_test_case('schemaorg-microdata.html')}
        rv = self.app.post('/validate-jobposting', data=data)
        assert rv.status == '200 OK'
        assert 'This job advert has clear information about the salary an applicant can expect' in rv.data

    def test_gender_coded_words(self):

        data = {'html': read_test_case('schemaorg-microdata.html')}
        rv = self.app.post('/validate-jobposting', data=data)
        assert rv.status == '200 OK'
        assert "This job ad doesn&#39;t use any words that are stereotypically masculine and stereotypically feminine. It probably won&#39;t be off-putting to men or women applicants." in rv.data

    def test_gender_coded_words(self):

        data = {'html': read_test_case('schemaorg-microdata.html')}
        rv = self.app.post('/validate-jobposting', data=data)
        assert rv.status == '200 OK'
        assert "This job ad doesn&#39;t use any words that are stereotypically masculine and stereotypically feminine. It probably won&#39;t be off-putting to men or women applicants." in rv.data

    def test_readability(self):

        data = {'html': read_test_case('schemaorg-microdata.html')}
        rv = self.app.post('/validate-jobposting', data=data)
        assert rv.status == '200 OK'
        print rv.data
        assert "The language in the description is difficult to read" in rv.data


    # def test_validate_jobposting_valid(self):
    #     url = 'http://www.w4mpjobs.org/JobDetails.aspx?jobid=56127'
    #     rv = self.app.get('/validate-jobposting?url=%s' % url)
    #     assert rv.status_code == 200
    #     assert 'Valid' in rv.data

    # def test_validate_jobposting_invalid(self):
    #     url = 'http://google.com'
    #     rv = self.app.get('/validate-jobposting?url=%s' % url)
    #     assert rv.status_code == 200
    #     assert 'Invalid' in rv.data

    # def test_validate_jobposting_bad_url(self):
    #     url = ''
    #     rv = self.app.get('/validate-jobposting?url=%s' % url)
    #     assert rv.status_code == 400
    #     assert 'Invalid URL' in rv.data

# if __name__ == '__main__':
#     unittest.main()