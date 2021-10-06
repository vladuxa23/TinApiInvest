from settings import *


class Config(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///capital.db'
    SECRET_KEY = secret_flask_key
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

#
# class DevelopmentConfig(Config):
#     DEBUG = True
#
#
# class TestingConfig(Config):
#     TESTING = True
