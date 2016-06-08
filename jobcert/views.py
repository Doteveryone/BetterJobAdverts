import requests
import os
import json
from flask import request, render_template, send_from_directory
from bs4 import BeautifulSoup
from jobcert import app
import job_posting
from parser import Parser

@app.route('/validate-jobposting', methods=['GET', 'POST'])
def validate_jobposting():

    #get html
    html = None
    if request.method == 'POST':
        html = request.values['html']

    if request.method == 'GET':
        html = requests.get(url, verify=False).content

    #parse
    parser = Parser()
    parser.parse(html)

    # result = None
    # status_code = 200
    # url = request.values['url']
    # job_postings = []

    # try:
    #     content = requests.get(url, verify=False).content
    #     soup = BeautifulSoup(content, "html.parser")
     
    #     # Look for any of the 3 types of JobPosting markups

    #     # Case 1: Microdata
    #     job_postings.extend(job_posting.from_microdata(content))

    #     # Case 2: RDFa
    #     job_postings.extend(job_posting.from_RDFa(content))

    #     # Case 3: JSON-LD
    #     job_postings.extend(job_posting.from_RDFa(content))
    #     ld_jsons = soup.findAll('script', {
    #         'type' : 'application/ld+json',
    #     })

    #     for ld in ld_jsons:
    #         print ld
    #         ld_json = json.loads(ld.string)
    #         # item = ld_json.get("@type", '') == "JobPosting"
    #         item = ld_json.get("@type", 'JobPosting')
    #         job_postings.append({'jobposting':item, 'format': 'ld-json'})

    #     if any(job_postings):
    #         result = 'passed'
    #     else:
    #         result = 'failed'

    # except requests.exceptions.MissingSchema:
    #     status_code = 400
    #     result = 'invalid url'
    # except requests.exceptions.ConnectionError:
    #     status_code = 400
    #     result = 'unable to reach url'

    return render_template('validate-jobposting.html', menu_item="index", parser=parser)

@app.route('/')
def index():
    return render_template('index.html', menu_item="index")

@app.route('/league-tables')
def league_tables():
    return render_template('league-tables.html', menu_item="league-tables")

@app.route('/about')
def about():
    return render_template('about.html', menu_item="about")

# @app.route('/tests/<path:path>')
# def tests(path):
#     root_dir = os.path.dirname(os.path.abspath(__file__)) 
#     return send_from_directory(os.path.join(root_dir, 'data', 'test-cases'), path)

# @app.route('/<path:path>')
# def home(path):
#     return send_from_directory(os.path.abspath('templates'), path)

