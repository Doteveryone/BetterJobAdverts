import json
import os
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.api import renderers
from flask.ext.api import FlaskAPI

app = Flask(__name__)
# CORS(app)

# class CORSRenderer(renderers.JSONRenderer):
#     def render(self, data, media_type, **options):
#         options['headers'].append('')
#         return super().render(data, media_type, **options)

import views

# if __name__ == "__main__":
#     app.run(debug=True)
