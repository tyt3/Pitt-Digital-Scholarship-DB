"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_mail import Mail, Message
from .models import *
from .database import db_session
from .controlled_vocab import *


# Initialize views Blueprint
views_bp = Blueprint('views_bp', __name__)

# Initialize Mail object
mail = Mail()

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

"""Function to Show Documentation Page"""
@views_bp.route('/documentation')
def documentation():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("documentation.html",
                           title="Documentation | Pitt Digital Scholarship Database",
                           user=current_user)

"""Function to Show Contact Page"""
@views_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        current_user.set_permissions()

    if request.method == "GET":
        return render_template("contact.html",
                           title="Contact Us | Pitt Digital Scholarship Database",
                           user=current_user)
    
    if request.method == "POST":
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg = Message(subject, sender='pittdsdb@gmail.com', recipients=['tyt3@pitt.edu'])
        msg.body = f"From: {full_name} <{email}> {message}" 
        mail.send(msg)

        return redirect(url_for('views_bp.index'))
    
    

"""Functions to Show Search Pages"""

# Initialize search variables for database values
areas = list(zip(*db_session.query(Area.area_name).distinct()))[0]
campuses = list(zip(*db_session.query(Address.campus).distinct()))[0]
career_levels = list(zip(*db_session.query(Funding.career_level).distinct()))[0]
funding_types = list(zip(*db_session.query(Funding.funding_type).distinct()))[0]
payment_types = list(zip(*db_session.query(Funding.payment_type).distinct()))[0]
methods = list(zip(*db_session.query(Method.method_name).distinct()))[0]
resources = list(zip(*db_session.query(Resource.resource_type).distinct()))[0]
support_types = list(zip(*db_session.query(Person.support_type).distinct()))[0]
tools = list(zip(*db_session.query(Tool.tool_name).distinct()))[0]

@views_bp.route('/search')
def search():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search.html",
                           title="Search | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-people', methods=['GET', 'POST'])
def search_people():
    if current_user.is_authenticated:
        current_user.set_permissions()

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        title = request.form.get('title')
        support_type = request.form.getlist('support_type')
        campus = request.form.getlist('campus')
    
    return render_template("search-people.html",
                           title="Search People| Pitt Digital Scholarship Database",
                           user=current_user,
                           campuses=campuses,
                           areas=areas,
                           methods=methods,
                           tools=tools,
                           support_types=support_types)

@views_bp.route('/search-units', methods=['GET', 'POST'])
def search_units():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-units.html",
                           title="Search Units| Pitt Digital Scholarship Database",
                           user=current_user,
                           campuses=campuses,
                           areas=areas,
                           resources=resources)

@views_bp.route('/search-areas', methods=['GET', 'POST'])
def search_areas():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-areas.html",
                           title="Search Areas| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-methods', methods=['GET', 'POST'])
def search_methods():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-methods.html", 
                           title="Search Methods| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-tools', methods=['GET', 'POST'])
def search_tools():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-tools.html",
                           title="Search Tools| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-resources', methods=['GET', 'POST'])
def search_resources():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-resources.html",
                           title="Search Resources| Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/search-funding', methods=['GET', 'POST'])
def search_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-funding.html",
                           title="Search Funding| Pitt Digital Scholarship Database",
                           user=current_user,
                           campuses=campuses,
                           funding_types=funding_types,
                           payment_types=payment_types,
                           career_levels=career_levels)

"""Functions to Show Add Pages"""
# Initialize add variables for database values
# see controlled_vocab.py

@views_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add.html",
                           title="Add Info | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-person', methods=['GET', 'POST'])
@login_required
def add_person():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-person.html",
                           title="Add a Person | Pitt Digital Scholarship Database",
                           user=current_user,
                           support_types=support_type)

@views_bp.route('/add-unit', methods=['GET', 'POST'])
@login_required
def add_unit():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-unit.html",
                           title="Add a Unit | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-area', methods=['GET', 'POST'])
@login_required
def add_area():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-area.html",
                           title="Add an Area | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-method', methods=['GET', 'POST'])
@login_required
def add_method():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-method.html",
                           title="Add a Method | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-tool', methods=['GET', 'POST'])
@login_required
def add_tool():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-tool.html",
                           title="Add a Tool | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-resource.html",
                           title="Add a Resource | Pitt Digital Scholarship Database",
                           user=current_user)

@views_bp.route('/add-funding', methods=['GET', 'POST'])
@login_required
def add_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    return render_template("add-funding.html",
                           title="Add a Funding Opportunity | Pitt Digital Scholarship Database",
                           user=current_user)
