"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, flash
from flask_session import Session
from .models import User
from flask_login import login_required, current_user


views_bp = Blueprint('views_bp', __name__)

"""Function to Show Homepage"""
@views_bp.route('/')
def index():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("index.html",
                           title="Pitt Digital Scholarship Database",
                           user=current_user)

"""Function to Show About Page"""
@views_bp.route('/about')
def about():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("about.html", 
                           title="Pitt Digital Scholarship Database",
                           user=current_user)

"""Functions to Show Search Pages"""
@views_bp.route('/search')
def search():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search.html",
                           title="Search | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-people')
def search_people():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-people.html",
                           title="Search People| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-units')
def search_units():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-units.html",
                           title="Search Units| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-areas')
def search_areas():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-areas.html",
                           title="Search Areas| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-methods')
def search_methods():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-methods.html", 
                           title="Search Methods| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-tools')
def search_tools():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-tools.html",
                           title="Search Tools| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-resources')
def search_resources():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-resources.html",
                           title="Search Resources| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-funding')
def search_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-funding.html",
                           title="Search Funding| Pitt Digital Scholarship Database",
                           user=current_user)

"""Functions to Show Add Pages"""
@views_bp.route('/add')
@login_required
def add():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add.html",
                           title="Add Info | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-person')
@login_required
def add_person():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-person.html",
                           title="Add a Person | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-unit')
@login_required
def add_unit():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-unit.html",
                           title="Add a Unit | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-area')
@login_required
def add_area():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-area.html",
                           title="Add an Area | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-method')
@login_required
def add_method():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-method.html",
                           title="Add a Method | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-tool')
@login_required
def add_tool():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-tool.html",
                           title="Add a Tool | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-resource')
@login_required
def add_resource():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-resource.html",
                           title="Add a Resource | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-funding')
@login_required
def add_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("add-funding.html",
                           title="Add a Funding Opportunity | Pitt Digital Scholarship Database",
                           user=current_user)

"""Function to Show Documentation Page"""
@views_bp.route('/documentation')
def documentation():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("documentation.html",
                           title="Documentation | Pitt Digital Scholarship Database",
                           user=current_user)

"""Function to Show Contact Page"""
@views_bp.route('/contact')
def contact():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("contact.html",
                           title="Contact Us | Pitt Digital Scholarship Database",
                           user=current_user)
