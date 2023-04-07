"""Module for creating Flask App"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
from database import db_session
import models
from views import views
from auth import auth
from api import api
from flask_marshmallow import Marshmallow

# Create a Flask Instance
app = Flask(__name__)

# Configure app
app.config.from_pyfile('config.py')

# Create marshmallow objects
ma = Marshmallow(app)

# Create api object
#API = Api(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Register Blueprints
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')


"""Run App"""
if __name__ == "__main__":
    app.run(debug=True)
