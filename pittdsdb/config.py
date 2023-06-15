from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = False
DEBUG = False
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

NEO4J_URI = environ.get('NEO4J_URI')
NEO4J_USER = environ.get('NEO4J_USER')             
NEO4J_PASSWORD = environ.get('NEO4J_PASSWORD')

# MAIL_SERVER = environ.get('MAIL_SERVER')
# MAIL_PORT = environ.get('MAIL_PORT')
# MAIL_USE_SSL = True
# MAIL_USE_TSL = True
# MAIL_USERNAME = environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
