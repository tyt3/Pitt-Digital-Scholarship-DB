from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

NEO4J_URI = environ.get('NEO4J_URI')
NEO4J_USER = environ.get('NEO4J_USER')             
NEO4J_PASSWORD = environ.get('NEO4J_PASSWORD')
