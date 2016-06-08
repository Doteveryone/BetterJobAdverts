import os
import unittest
from jobcert.parser import Parser

def read_test_case(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(root_dir, '../jobcert', 'data', 'test-cases', filename)
    return file(test_file).read()

class TestLicence(unittest.TestCase):

    def test_check_creative_commons_licence_head(self):
        licences = Parser.check_creative_commons_licence(read_test_case('licence-head.html'))
        assert licences == [{'name': 'Creative Commons Attribution', 'url': 'http://creativecommons.org/licenses/by-nd/4.0'}]

    def test_check_creative_commons_licence_link(self):
        licences = Parser.check_creative_commons_licence(read_test_case('licence-link.html'))
        assert licences == [{'name': 'Creative Commons Attribution', 'url': 'http://creativecommons.org/licenses/by-nd/4.0'}]

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

class TestParserLanguage(unittest.TestCase):

    def test_calculate_flesch_reading_ease(self):
        test_string = "The Australian platypus is seemingly a hybrid of a mammal and reptilian creature"
        assert 49.82 == Parser.calculate_flesch_reading_ease(test_string)

    def test_sentance_too_short_for_flesch_reading_ease(self):
        test_string = "A test"
        assert None == Parser.calculate_flesch_reading_ease(test_string)
