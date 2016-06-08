import json
from bs4 import BeautifulSoup
from textstat.textstat import textstat

class Parser():
    description = None
    results = []

    @staticmethod
    def check_creative_commons_licence(data):
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

        return licences

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
        return result

    def parse(self, data):
        self.results = []

        #is jobPosting?
        self.results.append(
          {
            'name': 'valid-jobposting',
            'result': self.has_jobposting(data),
          }
        )

        #How easy is the description to read?
        self.results.append(
          {
            'name': 'flesch-reading-ease',
            'result': self.calculate_flesch_reading_ease(data),
          }
        )

        #Is there a creative commons licence?
        self.results.append(
          {
            'name': 'creative-commons-licence',
            'result': self.check_creative_commons_licence(data),
          }
        )





