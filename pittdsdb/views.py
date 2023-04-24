"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from .database import db_session
from .models import *
from .add import *
from .get import *
from .controlled_vocab import vocab, existing

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
                           vocab=vocab,
                           existing=existing)


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


@views_bp.route('/add-person/<public_id>', methods=['GET', 'POST'])
@login_required
def add_person(public_id):
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
        affiliation = request.form.getlist('affiliation')
        unit = request.form.getlist('unit')
        department = request.form.getlist('department')
        subunit = request.form.getlist('subunit')
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

        person = Person.query.filter_by(public_id=public_id).first()

        if person:
            person.first_name = first_name
            person.last_name = request.form.get('last_name')
            person.pronouns = request.form.get('pronouns')
            person.title = request.form.get('title')
            person.affiliation = request.form.getlist('affiliation')
            person.unit = request.form.getlist('unit')
            person.department = request.form.getlist('department')
            person.subunit = request.form.getlist('subunit')
            person.email = request.form.get('email')
            person.web_address = request.form.get('web_address')
            person.phone = request.form.get('phone')
            person.scheduler_address = request.form.get('scheduler')
            person.building = request.form.get('building')
            person.office = request.form.get('office')
            person.street_address = request.form.get('street_address')
            person.city = request.form.get('city')
            person.state = request.form.get('state')
            person.zipcode = request.form.get('zipcode')
            person.campus = request.form.get('campus')
            person.preferred_contact = request.form.get('preferred_contact') 
            person.support_type = request.form.get('support_type')
            person.bio = request.form.get('bio')
            person.notes = request.form.get('notes')

            # Commit changes
            db_session.commit()

            return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
        else:
            new_person = add_person_to_db(first_name, last_name, title, 
                                            pronouns,  email, web_address, phone,
                                            scheduler_address, preferred_contact,
                                            support_type, bio, 
                                            current_user.get_id(), notes)
                                            
        
            # Check if the person was added succesfully
            if new_person:
                if new_person[0]:
                    # Get person object
                    p = new_person[1]
                    person_id = p.person_id
                    public_id = p.public_id

                    # Add affiliation
                    for a in affiliation:
                        add_person_affiliation(person_id, a)

                    # Add address
                    cursor = db_session.cursor()
                    cursor.callproc("sp_AddAddress", [person_id, "person", public_id,
                                                    building, office, street_address,
                                                    "", "", city, state, zipcode, 
                                                    campus, 0, 0])
                    address_added = list(cursor.fetchall()) # Get output params
                    if address_added[0]:
                        address_id = address_added[1]
                    cursor.close()

                    # Add units
                    for u in unit:
                        add_person_unit(person_id, u)
                    for s in subunit:
                        add_person_subunit(person_id, s)

                    # Add new person to database
                    db_session.add(new_person)

                    # Commit changes
                    db_session.commit()

                    return redirect(url_for('views_bp.view_person',
                                public_id=new_person.public_id))
            else:
                flash('The person record was not added. Please try again.',
                  category='error')
                
                return redirect(url_for('views_bp.add_person', 
                                        public_id=public_id))
            
    return render_template("add-person.html",
                           title="Add a Person | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           public_id=public_id)


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
                           user=current_user,
                           vocab=vocab,
                           existing=existing)


@views_bp.route('/add-area/<person_id>', methods=['GET', 'POST'])
@login_required
def add_area(person_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    if request.method == "POST":
        pass
        # area = request.form.get('area')
        # new_area = request.form.get('new_area')

        # if not area and not new_area:
        #     flash("Please select an existing area or add a new one.")
        # else:
        #     if area:
        #         pass
        #     if new_area:
        #         pass
        

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
    
    if request.method == "POST":
        method_name = request.form.get('method_name')
        proficiency = request.form.get('proficiency')

        method = Method.query.filter_by(method_name=method_name).first()

        # if method:
            

        #     # Commit changes
        #     db_session.commit()

        #     return redirect(url_for('views_bp.view_person',
        #                         public_id=person.public_id))
        # else:
        #     new_person = add_person_to_db(first_name, last_name, title, 
        #                                     pronouns,  email, web_address, phone,
        #                                     scheduler_address, preferred_contact,
        #                                     support_type, bio, 
        #                                     current_user.get_id(), notes)
                                            
        
        #     # Check if the person was added succesfully
        #     if new_person:
        #         if new_person[0]:
        #             # Get person object
        #             p = new_person[1]
        #             person_id = p.person_id
        #             public_id = p.public_id

        #             # Add affiliation
        #             for a in affiliation:
        #                 add_person_affiliation(person_id, a)

        #             # Add address
        #             cursor = db_session.cursor()
        #             cursor.callproc("sp_AddAddress", [person_id, "person", public_id,
        #                                             building, office, street_address,
        #                                             "", "", city, state, zipcode, 
        #                                             campus, 0, 0])
        #             address_added = list(cursor.fetchall()) # Get output params
        #             if address_added[0]:
        #                 address_id = address_added[1]
        #             cursor.close()

        #             # Add units
        #             for u in unit:
        #                 add_person_unit(person_id, u)
        #             for s in subunit:
        #                 add_person_subunit(person_id, s)

        #             # Add new person to database
        #             db_session.add(new_person)

            #         # Commit changes
            #         db_session.commit()

            #         return redirect(url_for('views_bp.view_person',
            #                     public_id=new_person.public_id))
            # else:
            #     flash('The person record was not added. Please try again.',
            #       category='error')
                
            #     return redirect(url_for('views_bp.add_method', 
            #                             public_id=public_id))

    return render_template("add-method.html",
                           title="Add a Method | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           public_id=public_id)


@views_bp.route('/add-tool/<person_id>', methods=['GET', 'POST'])
@login_required
def add_tool(person_id):
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
                           tool=None,
                           person_id=per)


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


"""Functions to Show View Pages"""
@views_bp.route('/view-person/<public_id>', methods=['GET', 'POST'])
def view_person(public_id):
    # Check if current user can update and/or delete person record
    user_can_update = user_can_delete = False

    if not current_user.is_anonymous and current_user.is_authenticated:
        current_user.set_permissions()
    
        if current_user.permission_level == 4:
            user_can_update = user_can_delete = True
        elif person.added_by == current_user.user_id:
            user_can_update = True
    else:
        print("logged out", user_can_delete, user_can_update)
    
    # Get person record
    person = db_session.query(Person).filter_by(public_id=public_id).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
              category="error")
        return render_template("index.html",
                           title="Pitt Digital Scholarship Database",
                           user=current_user)
    
    # get person support information
    person_support = get_person_support(person.person_id)
    
    # Get affiliation(s)
    person_affiliation = get_person_relations(person.person_id,
                                               "affiliation_type",
                                               "affiliation")

    # Get Unit information
    person_unit = get_person_relations(person.person_id,
                                       "unit_name", 
                                       "unit")

    # Get address
    person_address_result = get_person_relations(person.person_id,
                                                 "*",
                                                 "address")
    address_items = ['building_name', 'room_number', 'street_address', 
                 'address_2', 'address_3', 'city', 'state', 'zipcode', 'campus']
    person_address = {}
    i = 3
    for item in address_items:
        person_address[item] = person_address_result[i]
        i += 1
    
    return render_template("view-person.html",
                           title="View a Person | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           person=person,
                           person_affiliation=person_affiliation,
                           person_unit=person_unit,
                           person_support=person_support,
                           person_address=person_address,
                           user_can_update=user_can_update,
                           user_can_delete=user_can_delete)


@views_bp.route('/view-unit/<public_id>', methods=['GET', 'POST'])
def view_unit():
    if current_user.is_authenticated:
        current_user.set_permissions()
        
    return render_template("view-unit.html",
                           title="View a Unit | Pitt Digital Scholarship Database",
                           user=current_user)


@views_bp.route('/view-funding/<public_id>', methods=['GET', 'POST'])
def view_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
        
    return render_template("view-unit.html",
                           title="View a Funding Opportunity | Pitt Digital Scholarship Database",
                           user=current_user)


@views_bp.route('/test/<username>', methods=['GET', 'POST'])
def test(username):
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    user = User.query.filter_by(user_name=username).first()
    user_name = str(user.first_name) + " " + str(user.last_name)

       # user_name = current_user.user_name
    person_support = get_person_support(1)

    return render_template("test.html",
                           title="Test| Pitt Digital Scholarship Database",
                           user=current_user,
                           user_name=user_name,
                           vocab=vocab,
                           existing=existing,)


"""Functions to Show Update Pages"""

@views_bp.route('/update-area/<area_name>/<public_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def update_area(area_name, public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    person = Person.query.filter_by(public_id=public_id).first()
    area = Area.query.filter_by(area_name=area_name).first()
    notes = get_person_relations(person.person_id, 
                                 "fk_area_id", "area",
                                 area.area_id)[0]
    
    if request.method == "POST":
        updated_notes = request.form.get('notes')

        db_session.execute(f'UPDATE person_area \
                           SET notes = { updated_notes } \
                           WHERE user_id = { person.person_id }\
                           AND area_id = { area.area_id };')
        db_session.commit()

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    if request.method == "DELETE":
        db_session.execute(f'DELETE FROM person_area \
                           WHERE user_id = { person.person_id }\
                           AND area_id = { area.area_id };')
        db_session.commit()

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    return render_template("update-area.html",
                           title="Update an Area | Pitt Digital Scholarship Database",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           area=area,
                           notes=notes)


"""Functions to Delete Records"""
@views_bp.route('/delete-area/<area_id>/<person_id>', methods=['GET', 'POST'])
@login_required
def delete_area(area_id, person_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    person = Person.query.filter_by(person_id=person_id).first()
    area = Area.query.filter_by(area_id=area_id).first()
    
    db_session.execute(f'DELETE FROM person_area \
                        WHERE fk_person_id = { person.person_id }\
                        AND fk_area_id = { area.area_id };')
    db_session.commit()

    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))
