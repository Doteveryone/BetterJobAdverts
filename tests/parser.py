import os
import unittest
from jobcert.parser import Parser
from nose.tools import nottest

@nottest
def read_test_case(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(root_dir, '../jobcert', 'data', 'test-cases', filename)
    return file(test_file).read()

class TestLicence(unittest.TestCase):

    def test_check_creative_commons_licence_head(self):
        parser = Parser()
        parser.parse(read_test_case('licence-head.html'))
        assert parser.job_advert.creative_commons_licences == [{'name': 'Creative Commons Attribution', 'url': 'http://creativecommons.org/licenses/by-nd/4.0'}]

        assert parser.get_result('creative-commons-licence')['result'] == True

    def test_check_creative_commons_licence_link(self):
        parser = Parser()
        parser.parse(read_test_case('licence-link.html'))
        assert parser.job_advert.creative_commons_licences == [{'name': 'Creative Commons Attribution', 'url': 'http://creativecommons.org/licenses/by-nd/4.0'}]
        assert parser.get_result('creative-commons-licence')['result'] == True

class TestParserJsonld(unittest.TestCase):

    def test_publishing_format(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-jsonld.html'))
        assert parser.job_advert.publishing_format == "json-ld"

    def test_title(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-jsonld.html'))
        assert parser.job_advert.title == "Software Engineer"

    def test_description(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-jsonld.html'))
        assert parser.job_advert.description == "Description: ABC Company Inc. seeks a full-time mid-level software engineer to develop in-house tools."

class TestParserRdfa(unittest.TestCase):

    def test_publishing_format(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-rdfa.html'))
        assert parser.job_advert.publishing_format == "rdfa"

    def test_title(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-rdfa.html'))
        assert parser.job_advert.title == "Software Engineer"

    def test_description(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-rdfa.html'))
        assert parser.job_advert.description == """Description:
 
ABC Company Inc.

    seeks a full-time mid-level software engineer to develop in-house tools."""

class TestParserMicrodata(unittest.TestCase):

    def test_publishing_format(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html'))
        assert parser.job_advert.publishing_format == "microdata"

    def test_title(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html'))
        assert parser.job_advert.title == "Software Engineer"

    def test_description(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html'))
        assert parser.job_advert.description == """Description:
 
ABC Company Inc.

    seeks a full-time mid-level software engineer to develop in-house tools."""

    def test_salary_clear(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-salary-clear.html'))
        assert parser.get_result('salary-clarity')['result'] == 'clear'

    def test_salary_unclear(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-salary-unclear.html'))
        assert parser.get_result('salary-clarity')['result'] == 'unclear'

    def test_salary_missing(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-salary-missing.html'))
        assert parser.get_result('salary-clarity')['result'] == 'missing'

    def test_location_unclear(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html')) 
        assert parser.job_advert.address == 'Kirkland WA'

        assert parser.get_result('location-clarity')['result'] == 'unclear'

    def test_location_clear(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-location-clear-microdata.html')) 
        assert parser.job_advert.address == 'Somerset House, Strand, London WC2R 1LA'

        assert parser.get_result('location-clarity')['result'] == 'clear'

    def test_location_missing(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-location-missing-microdata.html')) 
        assert parser.job_advert.address == None

        assert parser.get_result('location-clarity')['result'] == 'missing'

    def test_employment_type(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html'))
        assert parser.job_advert.employment_type == 'Full-time'

        assert parser.get_result('has-employment-type')['result'] == True

    def test_employment_type_missing(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-employment-type-missing.html'))
        assert parser.get_result('has-employment-type')['result'] == False

class TestParserSchema(unittest.TestCase):

    def test_valid_jobPosting_microdata(self):
        assert True == Parser.has_jobposting(read_test_case('schemaorg-microdata.html'))

    def test_valid_jobPosting_jsonld(self):
        assert True == Parser.has_jobposting(read_test_case('schemaorg-jsonld.html'))

    def test_valid_jobPosting_rdfa(self):
        assert True == Parser.has_jobposting(read_test_case('schemaorg-rdfa.html'))

    def test_invalid_jobPosting_html(self):
        assert False == Parser.has_jobposting(read_test_case('schemaorg-html.html'))

    def test_invalid_jobPosting_text(self):
        assert False == Parser.has_jobposting(read_test_case('test.txt'))        

class TestParserGenderCoded(unittest.TestCase):

    def test_neutral(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-gender-coding-neutral.html'))
        assert parser.get_result('gender-coded-language')['result'] == 'neutral'

    def test_masculine(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-gender-coding-masculine.html'))
        assert 'masculine' in parser.get_result('gender-coded-language')['result']

    def test_feminine(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata-gender-coding-feminine.html'))
        assert 'feminine' in parser.get_result('gender-coded-language')['result']
        
class TestParserLanguage(unittest.TestCase):

    def test_parser(self):
        parser = Parser()
        parser.parse(read_test_case('schemaorg-microdata.html'))
        assert parser.get_result('flesch-reading-ease')['result']

    def test_calculate_flesch_reading_ease(self):
        test_string = "The Australian platypus is seemingly a hybrid of a mammal and reptilian creature"
        assert 49.82 == Parser.calculate_flesch_reading_ease(test_string)

    def test_sentance_too_short_for_flesch_reading_ease(self):
        test_string = "A test"
        assert None == Parser.calculate_flesch_reading_ease(test_string)
