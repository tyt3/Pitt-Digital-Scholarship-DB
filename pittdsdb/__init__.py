"""Module for creating Flask App"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_mail import Mail, Message
from datetime import datetime


def init_app():
    from .database import db_session
    from .views import views_bp, mail
    from .auth import auth_bp
    from .api import api_bp
    from .models import User
    from .schemas import ma

    # Create a Flask Instance
    app = Flask(__name__)

    # Configure app
    app.config.from_pyfile('config.py')

    login_manager = LoginManager()
    login_manager.login_view = 'auth_bp.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register function to tear down db session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Create api object
    api = Api(api_bp)

    # Initiate Mail object
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(views_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
