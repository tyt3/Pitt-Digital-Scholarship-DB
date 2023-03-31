"""Module for creating Flask App"""
from flask import Flask
from views import views
from auth import auth

# Create a Flask Instance
app = Flask(__name__)

# Configure app
app.config.from_pyfile('config.py')

# Register Blueprints
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


if __name__ == "__main__":
    app.run(debug=True)
