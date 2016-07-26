import datetime
from urlparse import urlparse
from jobcert import db

class Log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    checked_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    domain = db.Column(db.String(80))
    url = db.Column(db.Text())
    valid_jobposting = db.Column(db.String(80))
    publishing_format = db.Column(db.String(80))
    employment_type = db.Column(db.String(80))
    location_clarity = db.Column(db.String(80))
    salary_clarity = db.Column(db.String(80))
    creative_commons_licence = db.Column(db.String(80))
    gender_coded_language = db.Column(db.String(80))
    flesch_reading_ease = db.Column(db.Float())

    def populate_from_parser(self, url, parser):
        
        self.url = url
        if url:
            self.domain = urlparse(url)[1]

        self.valid_jobposting = parser.get_result('valid-jobposting')['result']
        self.publishing_format = parser.job_advert.publishing_format
        self.has_employment_type = parser.get_result('has-employment-type')['result']
        self.location_clarity = parser.get_result('location-clarity')['result']
        self.salary_clarity = parser.get_result('salary-clarity')['result']
        self.creative_commons_licence = parser.get_result('creative-commons-licence')['result']
        self.gender_coded_language = parser.get_result('gender-coded-language')['result']
        self.flesch_reading_ease = parser.get_result('flesch-reading-ease')['result']

    def __repr__(self):
        return '<Result %r %r>' % (self.name, self.domain)