from bs4 import BeautifulSoup
from textstat.textstat import textstat
import genderdecoder
import re
import json

def contains_postcode(data):

    data = data.replace(' ', '')

    inward = 'ABDEFGHJLNPQRSTUWXYZ'
    fst = 'ABCDEFGHIJKLMNOPRSTUWYZ'
    sec = 'ABCDEFGHKLMNOPQRSTUVWXY'
    thd = 'ABCDEFGHJKSTUW'
    fth = 'ABEHMNPRVWXY'

    if re.search('[%s][1-9]\d[%s][%s]$' % (fst, inward, inward), data) or \
        re.search('[%s][1-9]\d\d[%s][%s]$' % (fst, inward, inward), data) or \
        re.search('[%s][%s]\d\d[%s][%s]$' % (fst, sec, inward, inward), data) or \
        re.search('[%s][%s][1-9]\d\d[%s][%s]$' % (fst, sec, inward, inward), data) or \
        re.search('[%s][1-9][%s]\d[%s][%s]$' % (fst, thd, inward, inward), data) or \
        re.search('[%s][%s][1-9][%s]\d[%s][%s]$' % (fst, sec, fth, inward, inward), data):
        return True

    return False

def contains_numbers(data):
    return bool(re.search(r'\d', data))

class JobAdvert():
    title = None
    salary = None
    description = None
    address = None
    latlng = None
    employment_type = None
    publishing_format = None
    creative_commons_licences = []

    def to_text(self):
        return "%s" % (self.description)

    def to_dict(self):
        return {
            'title': self.title,
            'salary': self.salary,
            'description': self.description,
            'address': self.address,
            'employment_type': self.employment_type,
            'publishing_format': self.publishing_format,
            'creative_commons_licences': self.creative_commons_licences,
        }

class Parser():

    job_advert = None
    results = []

    def _parse_creative_commons_licence(self, data):
        licences = []
        soup = BeautifulSoup(data, "html5lib")

        #look in <head>
        for link in soup.find_all("link", attrs={"rel": "license"}):
            if '//creativecommons.org/licenses/' in link['href']:
                licences.append({'name':'', 'url': link['href']})

        #look for anchors
        for a in soup.find_all("a", attrs={"rel": "license"}):
            if '//creativecommons.org/licenses/' in a['href']:
                licences.append({'name':'', 'url': a['href']})

        for licence in licences:
            if '//creativecommons.org/licenses/by-nd/4.0' in licence['url']:
                licence['name'] = 'Creative Commons Attribution'
            elif '//creativecommons.org/licenses/by-nd' in licence['url']:
                licence['name'] = 'Creative Commons Attribution-NoDerivs'
            elif '//creativecommons.org/licenses/by-nc-sa' in licence['url']:
                licence['name'] = 'Attribution-NonCommercial-ShareAlike'
            elif '//creativecommons.org/licenses/by-sa' in licence['url']:
                licence['name'] = 'Attribution-ShareAlike'
            elif '//creativecommons.org/licenses/by-nc' in licence['url']:
                licence['name'] = 'Attribution-NonCommercial'
            elif '//creativecommons.org/licenses/by-nc-nd' in licence['url']:
                licence['name'] = 'Attribution-NonCommercial-NoDerivs'
            else:
                licence['name'] = 'Creative Commons (unable to determine exact licence)'            

        self.job_advert.creative_commons_licences = licences

    @staticmethod
    def calculate_flesch_reading_ease(data):
        try:
            return textstat.flesch_reading_ease(data)
        except TypeError:
            return None

    @staticmethod
    def has_jobposting(data):
        soup = BeautifulSoup(data, "html5lib")

        # Look for any of the 3 types of JobPosting markups
        job_posting_found = []

        # Case 1: Microdata
        job_posting_found.append(
            soup.findAll('div', {'itemtype' : 'http://schema.org/JobPosting'})
        )

        # Case 2: RDFa
        job_posting_found.append(
            soup.findAll('div', {
                'vocab' : 'http://schema.org/',
                'typeof': 'JobPosting',
            })
        )

        # Case 3: JSON-LD
        ld_jsons = soup.findAll('script', {
            'type' : 'application/ld+json',
        })
        for ld in ld_jsons:
            ld_json = json.loads(ld.string)
            job_posting_found.append(ld_json.get("@type", '') == "JobPosting")

        return any(job_posting_found)

    def get_result(self, name):
        """ Try and find a result based on a result name"""
        found = False
        for result in self.results:
            if result['name'] == name:
                found = result
                break
        return found

    def _parse_microdata(self, data):
        success = False
        soup = BeautifulSoup(data, "html5lib")
        job_advert = soup.find('div', {'itemtype' : 'http://schema.org/JobPosting'})
        if job_advert:
            success = True
            self.job_advert.publishing_format = 'microdata'

            #title
            title_element = job_advert.find(attrs={"itemprop": "title"})
            if title_element:
                self.job_advert.title = title_element.text

            #description
            description_element = job_advert.find(attrs={"itemprop": "description"})
            if description_element:
                self.job_advert.description = description_element.text

            #salary
            salary_currency_element = job_advert.find(attrs={"itemprop": "salaryCurrency"})
            base_salary_element = job_advert.find(attrs={"itemprop": "baseSalary"})

            salary = ""
            if salary_currency_element:
                salary = salary_currency_element.text
            if base_salary_element:
                if salary != "":
                    salary = "%s %s" % (salary, base_salary_element.text)
                else:
                    salary = base_salary_element.text
            self.job_advert.salary = salary

            #location
            location_element = job_advert.find(attrs={"itemprop": "jobLocation"})
            if location_element:
                address_element = location_element.find(attrs={"itemprop": "PostalAddress"})
                latitude_element = location_element.find(attrs={"itemprop": "latitude"})
                longitude_element = location_element.find(attrs={"itemprop": "longitude"})

                #address (if no address, just assume the whole contents)
                if address_element:
                    self.job_advert.address = address_element.text.strip()
                else:
                    self.job_advert.address = location_element.text.strip()

                #latlng
                if address_element and longitude_element:
                    self.latlng = [latitude_element.text, longitude_element.text]

            #Employment type
            employment_type_element = job_advert.find(attrs={"itemprop": "employmentType"})
            if employment_type_element:
                self.job_advert.employment_type = employment_type_element.text.strip()

        return success

    def _parse_rdfa(self, data):
        return False

    def _parse_jsonld(self, data):
        return False

    def _parse_html(self, data):
        return False

    def _analyse_format(self):
        #is jobPosting?
        self.results.append(
          {
            'name': 'valid-jobposting',
            'result': self.job_advert.publishing_format in ['microdata', 'rdfa', 'jsonld'],
            'explanation': '',
          }
        )

    def _analyse_text(self):

        #How easy is the description to read?
        self.results.append(
          {
            'name': 'flesch-reading-ease',
            'result': self.calculate_flesch_reading_ease(self.job_advert.to_text()),
            'explanation': '',
          }
        )

        #Gender-coded language
        gender_coded_result = genderdecoder.assess(self.job_advert.to_text())
        self.results.append(
          {
            'name': 'gender-coded-language',
            'result': gender_coded_result['result'],
            'explanation': gender_coded_result['explanation'],
          }
        )

    def _analyse_licence(self):
        #Is there a creative commons licence?
        self.results.append(
          {
            'name': 'creative-commons-licence',
            'result': len(self.job_advert.creative_commons_licences) > 0,
            'explanation': '',
          }
        )

    def _analyse_salary(self):
        #Is the salary clear?
        if self.job_advert.salary:
            if contains_numbers(self.job_advert.salary):
                salary_result = {
                    'name': 'salary-clarity',
                    'result': 'clear',
                    'explanation': '',
                }
            else:
                salary_result = {
                    'name': 'salary-clarity',
                    'result': 'unclear',
                    'explanation': '',
                }
        else:
            salary_result = {
                'name': 'salary-clarity',
                'result': 'missing',
                'explanation': '',
            }

        self.results.append(salary_result)

    def _analyse_location(self):
        if self.job_advert.address:
            if contains_postcode(self.job_advert.address):
                self.results.append(
                  {
                    'name': 'location-clarity',
                    'result': 'clear',
                    'explanation': '',
                  }
                )
            else:
                self.results.append(
                  {
                    'name': 'location-clarity',
                    'result': 'unclear',
                    'explanation': '',
                  }
                )
        else:
            self.results.append(
              {
                'name': 'location-clarity',
                'result': 'missing',
                'explanation': '',
              }
            )

    def _analyse_employment_type(self):

        self.results.append(
          {
            'name': 'has-employment-type',
            'result': self.job_advert.employment_type != None,
            'explanation': '',
          }
        )

    def analyse(self):

        self._analyse_format()
        self._analyse_text()
        self._analyse_licence()
        self._analyse_location()
        self._analyse_salary()
        self._analyse_employment_type()

    def parse(self, data):
        self.job_advert = JobAdvert()
        self.results = []

        #try various ways of parsing the job advert
        success = self._parse_microdata(data)
        if not success:
            success = self._parse_rdfa(data)
        if not success:
            success = self._parse_jsonld(data)
        if not success:
            success = self._parse_html(data)

        #parse licence
        self._parse_creative_commons_licence(data)        

        #analyse
        self.analyse()






