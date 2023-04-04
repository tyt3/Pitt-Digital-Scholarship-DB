"""Module for Views"""
from flask import Blueprint, render_template, request
import models

views = Blueprint('views', __name__)

"""Function to Show Homepage"""
@views.route('/')
def index():
    return render_template("index.html", title="Pitt Digital Scholarship Database")

"""Functions to Show Search Pages"""
@views.route('/search')
def search():
    return render_template("search.html", title="Search | Pitt Digital Scholarship Database")

@views.route('/search/people')
def search_people():
    return render_template("search/people.html", title="Search People| Pitt Digital Scholarship Database")

@views.route('/search/units')
def search_units():
    return render_template("search/units.html", title="Search Units| Pitt Digital Scholarship Database")

@views.route('/search/areas')
def search_areas():
    return render_template("search/areas.html", title="Search Areas| Pitt Digital Scholarship Database")

@views.route('/search/methods')
def search_methods():
    return render_template("search/methods.html", title="Search Methods| Pitt Digital Scholarship Database")

@views.route('/search/tools')
def search_tools():
    return render_template("search/tools.html", title="Search Tools| Pitt Digital Scholarship Database")

@views.route('/search/resources')
def search_resources():
    return render_template("search/resources.html", title="Search Resources| Pitt Digital Scholarship Database")

@views.route('/search/funding')
def search_funding():
    return render_template("search/funding.html", title="Search Funding| Pitt Digital Scholarship Database")

"""Function to Show Create Page"""
@views.route('/create')
def create():
    return render_template("create.html", title="Create | Pitt Digital Scholarship Database")
