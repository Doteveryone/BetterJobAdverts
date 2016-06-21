import json
import os
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.api import renderers
from flask.ext.api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.basicauth import BasicAuth


app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS', 'config.DevelopmentConfig'))
api = Api(app)
basic_auth = BasicAuth(app)
# db = SQLAlchemy(app)
# db.create_all()

import views
import api
import filters
# import models