"""Module for Views"""
from flask import Blueprint

views = Blueprint('views', __name__)

"""Function to Show Homepage"""
@views.route('/')
def home():
    return "<h1>Home</h1>"
