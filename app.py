"""Module for creating Flask App"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from views import views
from auth import auth
import models

# Create a Flask Instance
app = Flask(__name__)

# Configure app
app.config.from_pyfile('config.py')

# Create database object
db = SQLAlchemy(app)

# Register Blueprints
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


if __name__ == "__main__":
    app.run(debug=True)
