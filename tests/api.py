import unittest
from jobcert import app

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_require_url(self):
        rv = self.app.get('/api/check')
        assert "You must provide the url of a job" in rv.data
        assert rv.status_code == 400
