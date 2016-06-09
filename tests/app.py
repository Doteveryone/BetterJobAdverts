import unittest
from jobcert import app
import os

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