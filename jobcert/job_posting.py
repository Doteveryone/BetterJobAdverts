import json
import microdata
from pyld import jsonld
from bs4 import BeautifulSoup

class JobPosting(object):
    _original_format = None
    title = None

    # base_salary = None
    # date_posted = None
    # education_requirements = None
    # employment_type = None
    # experience_requirements = None
    # hiring_organization = None
    # incentive_compensation = None
    # industry = None
    # job_benefits = None
    # job_location = None
    # occupational_category = None
    # qualifications = None
    # responsibilities = None
    # salary_currency = None
    # skills = None
    # special_commitments = None
    # title = None
    # valid_through = None
    # work_hours = None
    # description = None
    # additional_type = None
    # alternate_name = None
    # description = None
    # disambiguating_description = None
    # image = None
    # main_entity_of_page = None
    # name = None
    # potential_action = None
    # sameAs = None
    # url = None

def from_microdata(content):
    result = []
    for item in microdata.get_items(content):
        if item.itemtype == [microdata.URI('http://schema.org/JobPosting')]:
            job_posting = JobPosting()
            job_posting.title = item.title
            job_posting._original_format = 'microdata'
            result.append(job_posting)
    return result

def from_RDFa(content):
    result = []
    soup = BeautifulSoup(content, "html.parser")
    for item in soup.findAll('div', {'vocab' : 'http://schema.org/','typeof': 'JobPosting',}):
        job_posting = JobPosting()
        job_posting.title = item.find(True, {"property" : "title"}).text.strip()
        job_posting._original_format = 'rdfa'
        result.append(job_posting)

    return result