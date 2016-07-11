import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', None)
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', None)
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', None)
    BASIC_AUTH_FORCE = True

class DevelopmentConfig(Config):
    API_BASE_URL = "http://localhost:5000/api"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SECRET_KEY = 'not-a-secret'
    BASIC_AUTH_FORCE = False

class TestConfig(DevelopmentConfig):
    TESTING = True