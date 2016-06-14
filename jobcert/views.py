import requests
import os
import json
from flask import request, render_template, send_from_directory
from bs4 import BeautifulSoup
from jobcert import app
import job_posting
from parser import Parser

@app.route('/check', methods=['GET', 'POST'])
def validate_jobposting():

    #get html
    error = False
    html = None
    url = None
    if request.method == 'POST':
        html = request.values['html']

    if request.method == 'GET':
        url = request.values['url']
        try:
            html = requests.get(url, verify=False).content
        except requests.exceptions.ConnectionError:
            error = "Sorry, that URL does not exist"
        except requests.exceptions.HTTPError:
            error = "Sorry, something went wrong"
        except requests.exceptions.Timeout:
            error = "Sorry, there was a timeout when trying to visit that URL"

    #parse
    parser = Parser()
    if error == False:
        parser.parse(html)

    return render_template('validate-jobposting.html', menu_item="index", parser=parser, error=error, url=url)

@app.route('/')
def index():
    return render_template('index.html', menu_item="index")

@app.route('/data')
def league_tables():
    return render_template('league-tables.html', menu_item="league-tables")

@app.route('/about')
def about():
    return render_template('about.html', menu_item="about")

@app.route('/api')
def api():
    return render_template('api.html', menu_item="api")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
# @app.route('/tests/<path:path>')
# def tests(path):
#     root_dir = os.path.dirname(os.path.abspath(__file__)) 
#     return send_from_directory(os.path.join(root_dir, 'data', 'test-cases'), path)

# @app.route('/<path:path>')
# def home(path):
#     return send_from_directory(os.path.abspath('templates'), path)

