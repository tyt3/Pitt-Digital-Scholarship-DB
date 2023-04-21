"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_mail import Mail, Message
from .models import *
from .database import db_session
from .controlled_vocab import vocab, existing
from .add import *


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
                           existing=existing)

@views_bp.route('/search-units', methods=['GET', 'POST'])
def search_units():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search-units.html",
                           title="Search Units| Pitt Digital Scholarship Database",
                           user=current_user,
                           existing=existing)

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
                           existing=existing)

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
    
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pronouns = request.form.get('pronouns')
        title = request.form.get('title')
        affiliation = request.form.get('affiliation')
        unit = request.form.get('unit')
        department = request.form.get('department')
        subunit = request.form.get('subunit')
        email = request.form.get('email')
        web_address = request.form.get('web_address')
        phone = request.form.get('phone')
        scheduler_address = request.form.get('scheduler')
        building = request.form.get('building')
        office = request.form.get('office')
        street_address = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        campus = request.form.get('campus')
        preferred_contact = request.form.get('preferred_contact') 
        support_type = request.form.get('support_type')
        bio = request.form.get('bio')
        notes = request.form.get('notes')

        person_added = add_person_to_db(first_name, last_name, title, pronouns, 
                                        email, web_address, phone, 
                                        scheduler_address, preferred_contact,
                                        support_type, bio, 
                                        current_user.get_id(), notes)
        
        # Check if the person was added succesfully
        if person_added[0]:
            # Get person object
            p = person_added[1]
            person_id = p.person_id
            public_id = p.public_id

            # Add address
            cursor = db_session.cursor()
            cursor.callproc("sp_AddAddress", [person_id, "person", public_id,
                                              building, office, street_address,
                                              "", "", city, state, zipcode, 
                                              campus, 0, 0])
            address_added = list(cursor.fetchall())

            address_id = -1
            if address_added[0]:
                address_id = address_added[1]
            cursor.close()
            db_session.commit()

            # Add relationships


            
        else:
            flash('The person record was not added. Please try again.',
                  category='error')
            
            return redirect(url_for('views_bp.add_person'))
            
    return render_template("add-person.html",
                           title="Add a Person | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing)

@views_bp.route('/add-unit', methods=['GET', 'POST'])
@login_required
def add_unit():
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions()

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get data from form and submit to database
    if request.method == "POST":
        email = request.form.get('email')

        return render_template("/add-unit.html",
                               user=current_user,
                               vocab=vocab,
                               existing=existing)
        
    return render_template("/add-unit.html",
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
    if request.method == "POST":
        area = request.form.get('area')
        new_area = request.form.get('new_area')

        if not area and not new_area:
            flash("Please select an existing area or add a new one.")

    return render_template("test.html",
                           title="Add an Area | Pitt Digital Scholarship Database",
                           user=current_user,
                           existing=existing,
                           vocab=vocab)

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
                           user=current_user,
                           vocab=vocab,
                           existing=existing)

@views_bp.route('/add-tool', methods=['GET', 'POST'])
@login_required
def add_tool():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    if request.method == "POST":
        pass

    return render_template("add-tool.html",
                           title="Add a Tool | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           tool=None)

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

@views_bp.route('/test', methods=['GET', 'POST'])
def test():
   
    return render_template("test.html",
                           title="Test| Pitt Digital Scholarship Database",
                           user=None,
                           vocab=vocab,
                           existing=existing)

@views_bp.route('/view-unit', methods=['GET', 'POST'])
def view_unit():
    if current_user.is_authenticated:
        current_user.set_permissions()
        
    return render_template("view-unit.html",
                           title="View a Unit | Pitt Digital Scholarship Database",
                           user=current_user)