"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session
from flask_session import Session


views_bp = Blueprint('views_bp', __name__)

"""Function to Show Homepage"""
@views_bp.route('/')
def index():
    can_add = False
    can_update_all = False
    can_delete = False
    can_update_created = False
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first_or_404()
        if user.permission_level == 4:
            can_add = True
            can_update = True
            can_update_created = True
            can_delete= True
            can_search = True
        elif user.permission_level == 3:
            can_add = True
            can_update_all = True
            can_update_created = True
        elif user.permission_level == 2:
            can_add = True
            can_update_created = True
    return render_template("index.html", title="Pitt Digital Scholarship Database", can_add=can_add, can_delete = can_delete, can_update_all = can_update_all, can_update_created = can_update_created)

"""Function to Show About Page"""
@views_bp.route('/about')
def about():
    return render_template("about.html", title="Pitt Digital Scholarship Database")

"""Functions to Show Search Pages"""
@views_bp.route('/search')
def search():
    return render_template("search.html", title="Search | Pitt Digital Scholarship Database")

@views_bp.route('/search/people')
def search_people():
    return render_template("search/people.html", title="Search People| Pitt Digital Scholarship Database")

@views_bp.route('/search/units')
def search_units():
    return render_template("search/units.html", title="Search Units| Pitt Digital Scholarship Database")

@views_bp.route('/search/areas')
def search_areas():
    return render_template("search/areas.html", title="Search Areas| Pitt Digital Scholarship Database")

@views_bp.route('/search/methods')
def search_methods():
    return render_template("search/methods.html", title="Search Methods| Pitt Digital Scholarship Database")

@views_bp.route('/search/tools')
def search_tools():
    return render_template("search/tools.html", title="Search Tools| Pitt Digital Scholarship Database")

@views_bp.route('/search/resources')
def search_resources():
    return render_template("search/resources.html", title="Search Resources| Pitt Digital Scholarship Database")

@views_bp.route('/search/funding')
def search_funding():
    return render_template("search/funding.html", title="Search Funding| Pitt Digital Scholarship Database")

"""Functions to Show Add Pages"""
@views_bp.route('/add')
def add():
    return render_template("add.html", title="Add Info | Pitt Digital Scholarship Database")

@views_bp.route('/add/person')
def add_person():
    return render_template("add/person.html", title="Add a Person | Pitt Digital Scholarship Database")

@views_bp.route('/add/unit')
def add_unit():
    return render_template("add/unit.html", title="Add a Unit | Pitt Digital Scholarship Database")

@views_bp.route('/add/area')
def add_area():
    return render_template("add/area.html", title="Add an Area | Pitt Digital Scholarship Database")

@views_bp.route('/add/method')
def add_method():
    return render_template("add/method.html", title="Add a Method | Pitt Digital Scholarship Database")

@views_bp.route('/add/tool')
def add_tool():
    return render_template("add/tool.html", title="Add a Tool | Pitt Digital Scholarship Database")

@views_bp.route('/add/resource')
def add_resource():
    return render_template("add/resource.html", title="Add a Resource | Pitt Digital Scholarship Database")

@views_bp.route('/add/funding')
def add_funding():
    return render_template("add/funding.html", title="Add a Funding Opportunity | Pitt Digital Scholarship Database")

"""Function to Show Documentation Page"""
@views_bp.route('/documentation')
def documentation():
    return render_template("documentation.html", title="Documentation | Pitt Digital Scholarship Database")

"""Function to Show Contact Page"""
@views_bp.route('/contact')
def contact():
    return render_template("contact.html", title="Contact Us | Pitt Digital Scholarship Database")