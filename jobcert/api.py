from flask_restful import Resource, reqparse, inputs
from jobcert import app, api
from parser import Parser
import requests
import json

class CheckApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(CheckApi, self).__init__()

    def post (self):
        self.parser.add_argument('html', type=str, required=True, location=('json', 'values'), help="You must provide some HTML")
        args = self.parser.parse_args()
        parser = Parser()
        parser.parse(args['html'])
        return {
          'job_advert': parser.job_advert.to_dict(),
          'analysis': parser.results
          }, 200

    def get(self):

        self.parser.add_argument('url', type=inputs.url, required=True, location='values', help="You must provide the url of a job")
        args = self.parser.parse_args()

        try:
            html = requests.get(args['url'], verify=False).content
            parser = Parser()
            parser.parse(html)
            return {
              'job_advert': parser.job_advert.to_dict(),
              'analysis': parser.results
              }, 200
            
        except requests.exceptions.ConnectionError:
            error = "Sorry, that URL does not exist", 400
        except requests.exceptions.HTTPError:
            error = "Sorry, something went wrong", 502
        except requests.exceptions.Timeout:
            error = "Sorry, there was a timeout when trying to visit that URL", 502


api.add_resource(CheckApi, '/api/check')