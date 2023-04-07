"""Module for creating Flask App"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
from .database import db_session
from .views import views_bp
from .auth import auth_bp
from .api import api_bp
from flask_marshmallow import Marshmallow


def init_app():
    # Create a Flask Instance
    app = Flask(__name__)

    # Configure app
    app.config.from_pyfile('config.py')

    # Create marshmallow objects
    ma = Marshmallow(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Create api object
    api = Api(api_bp)

    # Register Blueprints
    app.register_blueprint(views_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
