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

    if re.search('[%s][1-9]\d[%s][%s]' % (fst, inward, inward), data) or \
        re.search('[%s][1-9]\d\d[%s][%s]' % (fst, inward, inward), data) or \
        re.search('[%s][%s]\d\d[%s][%s]' % (fst, sec, inward, inward), data) or \
        re.search('[%s][%s][1-9]\d\d[%s][%s]' % (fst, sec, inward, inward), data) or \
        re.search('[%s][1-9][%s]\d[%s][%s]' % (fst, thd, inward, inward), data) or \
        re.search('[%s][%s][1-9][%s]\d[%s][%s]' % (fst, sec, fth, inward, inward), data):
        return True

    return False

def contains_numbers(data):
    return bool(re.search(r'\d', data))

def element_content(element):
    result = None
    if element:
        if element.text != '':
            result = element.text.strip()
        elif element.get('content'):
            result = element['content'].strip()
    return result

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
            soup.findAll(attrs={'itemtype' : 'http://schema.org/JobPosting'})
        )
        job_posting_found.append(
            soup.findAll(attrs={'itemtype' : 'https://schema.org/JobPosting'})
        )

        # Case 2: RDFa
        job_posting_found.append(
            soup.findAll(attrs={
                'vocab' : 'http://schema.org/',
                'typeof': 'JobPosting',
            })
        )
        job_posting_found.append(
            soup.findAll(attrs={
                'vocab' : 'https://schema.org/',
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

    def _parse_html(self, job_advert, attribute_name):
        #used for rdfa and microdata

        #title
        title_element = job_advert.find(attrs={attribute_name: "title"})
        self.job_advert.title = element_content(title_element)

        #description
        description_element = job_advert.find(attrs={attribute_name: "description"})
        if description_element:
            self.job_advert.description = "\n".join(description_element.strings).strip()

        #salary
        salary_currency_element = job_advert.find(attrs={attribute_name: "salaryCurrency"})
        base_salary_element = job_advert.find(attrs={attribute_name: "baseSalary"})

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
        location_element = job_advert.find(attrs={attribute_name: "jobLocation"})
        if location_element:
            address_element = location_element.find(attrs={attribute_name: "PostalAddress"})
            latitude_element = location_element.find(attrs={attribute_name: "latitude"})
            longitude_element = location_element.find(attrs={attribute_name: "longitude"})

            #address (if no address, just assume the whole contents)
            if address_element:
                self.job_advert.address = address_element.text.strip()
            else:
                self.job_advert.address = location_element.text.strip()

            #latlng
            if longitude_element:
                self.job_advert.latlng = [latitude_element.text, longitude_element.text]

        #Employment type
        employment_type_element = job_advert.find(attrs={attribute_name: "employmentType"})
        if employment_type_element:
            self.job_advert.employment_type = employment_type_element.text.strip()

    def _parse_microdata(self, data):
        success = False
        soup = BeautifulSoup(data, "html5lib")

        job_advert = soup.find(attrs={'itemtype' : 'http://schema.org/JobPosting'})

        if not job_advert:
            job_advert =  soup.find(attrs={'itemtype' : 'https://schema.org/JobPosting'})


        if job_advert:
            success = True
            self.job_advert.publishing_format = 'microdata'

            self._parse_html(job_advert, "itemprop")

        return success

    def _parse_rdfa(self, data):
        success = False
        soup = BeautifulSoup(data, "html5lib")
        job_advert = soup.find(attrs={
                'vocab' : 'http://schema.org/',
                'typeof': 'JobPosting',
            })
        if not job_advert:
            job_advert = soup.find(attrs={
                'vocab' : 'https://schema.org/',
                'typeof': 'JobPosting',
            })

        if job_advert:
            success = True
            self.job_advert.publishing_format = 'rdfa'

            self._parse_html(job_advert, "property")

        return success

    def _parse_jsonld(self, data):
        success = False
        soup = BeautifulSoup(data, "html5lib")
        job_advert = soup.find('script', {
            'type' : 'application/ld+json',
        })
        if job_advert:
            success = True
            self.job_advert.publishing_format = 'json-ld'
            data = json.loads(job_advert.text)

            #title
            if data.get('title', False):
                self.job_advert.title = data['title']

            #description
            if data.get('description', False):
                self.job_advert.description = data['description']

            #salary
            if data.get('baseSalary', False):
                salary = "%s %s" % (data.get('salaryCurrency', False), data.get('baseSalary', False))
                salary = salary.strip()
                if salary != "":
                    self.job_advert.salary = salary.strip()

            if data.get('jobLocation', False):

                #address
                if data['jobLocation'].get('address', False):
                    address = ""
                    for k,v in data['jobLocation']['address'].iteritems():
                        if k != '@type':
                            address += (v + ", ")
                    address = re.sub(', $', '', address)
                    self.job_advert.address = str(address).strip()

                #latlng
                if data['jobLocation'].get('geo', False):
                    self.job_advert.latlng = [data['latitude'], data['longitude']]

            #description
            if data.get('employmentType', False):
                self.job_advert.employment_type = data['employmentType']

        return success

    def _analyse_format(self):
        #is jobPosting + minimum information
        result = "missing"
        if self.job_advert.publishing_format in ['microdata', 'rdfa', 'jsonld']:
            if self.job_advert.description and self.job_advert.address and self.job_advert.salary and self.job_advert.employment_type:
                result = "yes"
            else:
                result = "incomplete"

        self.results.append(
          {
            'name': 'valid-jobposting',
            'result': result,
            'explanation': '',
            'data': {},
          }
        )

    def _analyse_text(self):

        #How easy is the description to read?
        self.results.append(
          {
            'name': 'flesch-reading-ease',
            'result': self.calculate_flesch_reading_ease(self.job_advert.to_text()),
            'explanation': '',
            'data': {},
          }
        )

        #Gender-coded language (if longer than 100 chars)
        if len(self.job_advert.to_text()) > 100:
            gender_coded_result = genderdecoder.assess(self.job_advert.to_text())
            self.results.append(
              {
                'name': 'gender-coded-language',
                'result': gender_coded_result['result'],
                'explanation': gender_coded_result['explanation'],
                'data': {
                    'masculine_coded_words': gender_coded_result['masculine_coded_words'],
                    'feminine_coded_words': gender_coded_result['feminine_coded_words']
                    },
              }
            )
        else:
            self.results.append(
              {
                'name': 'gender-coded-language',
                'result': None,
                'explanation': None,
                'data': {},
              }
            )

    def _analyse_licence(self):
        #Is there a creative commons licence?
        self.results.append(
          {
            'name': 'creative-commons-licence',
            'result': len(self.job_advert.creative_commons_licences) > 0,
            'explanation': '',
            'data': {},
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
                    'data': {},
                }
            else:
                salary_result = {
                    'name': 'salary-clarity',
                    'result': 'unclear',
                    'explanation': '',
                    'data': {},
                }
        else:
            salary_result = {
                'name': 'salary-clarity',
                'result': 'missing',
                'explanation': '',
                'data': {},
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
                    'data': {},
                  }
                )
            else:
                self.results.append(
                  {
                    'name': 'location-clarity',
                    'result': 'unclear',
                    'explanation': '',
                    'data': {},
                  }
                )
        else:
            self.results.append(
              {
                'name': 'location-clarity',
                'result': 'missing',
                'explanation': '',
                'data': {},
              }
            )

    def _analyse_employment_type(self):

        self.results.append(
          {
            'name': 'has-employment-type',
            'result': self.job_advert.employment_type != None,
            'explanation': '',
            'data': {},
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

        #parse licence
        self._parse_creative_commons_licence(data)        

        #analyse
        self.analyse()


