"""Module for Views"""
from flask import Blueprint, render_template, request
import models

views = Blueprint('views', __name__)

"""Function to Show Homepage"""
@views.route('/')
def index():
    return render_template("index.html", title="Pitt Digital Scholarship Database")

"""Function to Show Search Page"""
@views.route('/search')
def search():
    return render_template("search.html", title="Search | Pitt Digital Scholarship Database")

"""Function to Show Create Page"""
@views.route('/create')
def create():
    return render_template("create.html", title="Create | Pitt Digital Scholarship Database")
