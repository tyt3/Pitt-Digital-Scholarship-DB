"""Module for Views"""
from flask import Blueprint, render_template, request
import models

views = Blueprint('views', __name__)

"""Function to Show Homepage"""
@views.route('/')
def home():
    return render_template("index.html", title="Pitt Digital Scholarship Database")

"""Function to Show Search Page"""
@views.route('/search')
def search():
    return "<h1>Search</h1>"

"""Function to Show Create Page"""
@views.route('/create')
def create():
    return "<h1>Search</h1>"