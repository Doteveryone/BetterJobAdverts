import os

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', None)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SECRET_KEY = 'not-a-secret'

class TestConfig(DevelopmentConfig):
    TESTING = True