"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_required, current_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from .database import db_session
from .models import *
from .get import *
from .add import *
from .delete import *
from .networkdb import *
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
        subunit = request.form.getlist('subunit')
        email = request.form.get('email')
        web_address = request.form.get('web_address')
        phone = request.form.get('phone')
        scheduler_address = request.form.get('scheduler')
        other_contact = request.form.get('other_contact')
        # building = request.form.get('building')
        # office = request.form.get('office')
        # street_address = request.form.get('street_address')
        # city = request.form.get('city')
        # state = request.form.get('state')
        # zipcode = request.form.get('zipcode')
        # campus = request.form.get('campus')
        preferred_contact = request.form.get('preferred_contact') 
        support_type = request.form.get('support_type')
        bio = request.form.get('bio')
        notes = request.form.get('notes')
        photo_url = request.form.get('photo_url')

        person = Person.query.filter_by(public_id=public_id).first()

        if person:
            person.first_name = first_name
            person.last_name = last_name
            person.pronouns = pronouns
            person.title = title
            person.affiliation = affiliation # add functionality to remove affiliations in db
            person.unit = unit
            person.subunit = subunit
            person.email = email
            person.web_address = web_address
            person.phone = phone
            person.scheduler_address = scheduler_address
            # person.building = building
            # person.office = office
            # person.street_address = street_address
            # person.city = city
            # person.state = state
            # person.zipcode = zipcode
            # person.campus = campus
            person.preferred_contact = preferred_contact 
            person.support_type = support_type
            person.bio = bio
            person.notes = notes
            person.photo_url = photo_url

            # Update affiliations
            delete_affiliations(person.person_id)
            for a in affiliation:
                add_person_affiliation(person.person_id, a)

            # Commit changes
            db_session.commit()

            #Update graph node
            update_person_node(first_name + ' ' + last_name, public_id)

            return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
        else:
            new_person = add_person_to_db(first_name, last_name, title, 
                                            pronouns, email, web_address, phone,
                                            scheduler_address, other_contact,
                                            preferred_contact, support_type, 
                                            bio, current_user.get_id(), notes,
                                            photo_url)
                                            
        
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

                    # # Add new person to database
                    # db_session.add(new_person)

                    # # Commit changes
                    # db_session.commit()

                    # Add Person Node
                    add_person_node(first_name + ' ' + last_name, public_id)

                    return redirect(url_for('views_bp.view_person',
                                public_id=public_id))
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


@views_bp.route('/add-person-unit/<public_id>', 
                methods=['POST'])
@login_required
def add_person_unit(public_id):
    person = Person.query.filter_by(public_id=public_id).first()
    
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions()

        if current_user.permission_level == 4:
            user_can_update = user_can_delete = True
        elif person.added_by == current_user.user_id:
            user_can_update = True

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    if request.method == "POST":
        # Get data from form and submit to database
        unit_name = request.form.get('unit_name')
        parent_unit_name = request.form.get('parent_unit_name')

        # Add unit(s)
        if parent_unit_name == "None":
            add_person_unit_to_db(person.person_id, parent_unit_name)
        else:
            add_person_subunit_to_db(person.person_id, unit_name)
            add_person_unit_to_db(person.person_id, parent_unit_name)

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    


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


@views_bp.route('/add-area/<public_id>', methods=['POST'])
@login_required
def add_area(public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get form values
    area_name = request.form.get('area')
    new_area_name = request.form.get('new_area').title()
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    person = Person.query.filter_by(public_id=public_id).first()
    area = None
    proficiency = Proficiency.query.filter_by(proficiency_level=proficiency_level).first()

    if new_area_name:
        existing_area = Area.query.filter_by(area_name=new_area_name).first()

        if existing_area:
            flash("That area already exists!", category='error')
        else:
            area = add_area_to_db(new_area_name)

            # Add Area node
            add_area_node(new_area_name)

            # Update area name to the new area
            area_name = new_area_name

    # Add person-person area relationships
    area = Area.query.filter_by(area_name=area_name).first()
    add_person_support(person.person_id, "area", area.area_id,
                               proficiency.proficiency_id, notes, True)
    add_person_support_combos(person.person_id, area.area_id)
    attach_person_area(public_id, area_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-method/<public_id>', methods=['POST'])
@login_required
def add_method(public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get form values
    area_name = request.form.getlist('area')
    method_name = request.form.get('method')
    new_method_name = request.form.get('new_method')
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    # Get object information
    person = Person.query.filter_by(public_id=public_id).first()
    method = None
    proficiency = Proficiency.query.filter_by(proficiency_level=proficiency_level).first()

    # Add method and relations
    if new_method_name:
        # Make sure the method name being added doesn't already exist
        existing_method = Method.query.filter_by(method_name=new_method_name).first()
        if existing_method:
            flash("That method already exists!", category='error')
        else:
            method = add_method_to_db(new_method_name)
    else:
        # Get existing method
        method = Method.query.filter_by(method_name=method_name).first()
    
    # Add person-support relationships
    add_person_support(person.person_id, "method", method.method_id,
                            proficiency.proficiency_id, notes, True)
    for name in area_name:
        area = Area.query.filter_by(area_name=name).first()
        add_person_support_combos(person.person_id, area.area_id, 
                                    method.method_id)

    result = get_relations("Person", "public_id", person.public_id, "Area", "name", area.area_name)
    if len(result) == 0:
        attach_person_area(person.public_id, area.area_name)
    result = get_relations("Person", "public_id", person.public_id, "Method", "name", method.method_name)
    if len(result) == 0:
        attach_person_method(person.public_id, method.method_name)
    result = get_relations("Area", "name", area.area_name, "Method", "name", method.method_name)
    if len(result) == 0:
        attach_area_method(area.area_name, method.method_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-tool/<public_id>', methods=['POST'])
@login_required
def add_tool(public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get form values
    area_name = request.form.getlist('area')
    method_name = request.form.getlist('method')
    tool_name = request.form.get('tool')
    new_tool_name = request.form.get('new_tool')
    tool_type = request.form.get('tool_type')
    web_address = request.form.get('web_address')
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    # Create db record objects
    person = Person.query.filter_by(public_id=public_id).first()
    tool = None
    proficiency = Proficiency.query.filter_by(proficiency_level=proficiency_level).first()

    # Check if new_tool_name was input in form
    if new_tool_name:
        # Make sure the tool name being added doesn't already exist
        existing_tool = Tool.query.filter_by(tool_name=new_tool_name).first()
        if existing_tool:
            flash("That tool already exists!", category='error')
            return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
        else:
            tool = add_tool_to_db(new_tool_name, tool_type, web_address)
    else:
        # Get existing tool
        tool = Tool.query.filter_by(tool_name=tool_name).first()
    
    # Add person-support relationships
    add_person_support(person.person_id, "tool", tool.tool_id,
                            proficiency.proficiency_id, notes, True)
    for a_name in area_name:
        area = Area.query.filter_by(area_name=a_name).first()
        for m_name in method_name:
            method = Method.query.filter_by(method_name=m_name).first()
            add_person_support_combos(person.person_id, area.area_id, 
                                        method.method_id, tool.tool_id)
    result = get_relations("Person", "name", person.public_id, "Area", "name", area.area_name)
    if len(result) == 0:
        attach_person_area(person.public_id, area.area_name)
    result = get_relations("Person", "name", person.public_id, "Method", "name", method.method_name)
    if len(result) == 0:
        attach_person_method(person.public_id, method.method_name)
    result = get_relations("Person", "name", person.public_id, "Tool", "name", tool.tool_name)
    if len(result) == 0:
        attach_person_tool(person.public_id, tool.tool_name)

    # attach area to method if not exists
    result = get_relations("Area", "name", area.area_name, "Method", "name", method.method_name)
    if len(result) == 0:
        attach_area_method(area.area_name, method.method_name)
    # attach tool to method if not exists
    result = get_relations("Tool", "name", tool.tool_name, "Method", "name", method.method_name)
    if len(result) == 0:
        attach_tool_method(tool.tool_name, method.method_name)
    # attach tool to area if not exists
    result = get_relations("Area", "name", area.area_name, "Tool", "name", tool.tool_name)
    if len(result) == 0:
        attach_area_tool(area.area_name, tool.tool_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-resource', methods=['POST'])
@login_required
def add_resource(public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    person = Person.query.filter_by(public_id=public_id).first()
    
    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-funding', methods=['GET', 'POST'])
@login_required
def add_funding():
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    
    return render_template("/add-funding.html",
                           title="Add a Funding Opportunity | Pitt Digital Scholarship Database",
                           user=current_user,
                           vocab=vocab,
                           existing=existing)


"""Functions to Show Update Pages"""

@views_bp.route('/update-area/<area_name>/<public_id>', methods=['GET', 'POST'])
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
                                 "notes", "area",
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

    return render_template("update-area.html",
                           title="Update an Area | Pitt Digital Scholarship Database",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           area=area,
                           notes=notes)


@views_bp.route('/update-method/<method_name>/<public_id>', methods=['GET', 'POST'])
@login_required
def update_method(method_name, public_id):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    person = Person.query.filter_by(public_id=public_id).first()
    method = Method.query.filter_by(method_name=method_name).first()
    notes = get_person_relations(person.person_id, 
                                 "notes", "method",
                                 method.method_id)[0]
    
    if request.method == "POST":
        updated_proficiency = request.form.get('notes')
        updated_notes = request.form.get('notes')

        db_session.execute(f'UPDATE person_area \
                           SET notes = { updated_notes } \
                           WHERE user_id = { person.person_id }\
                           AND area_id = { method.method_id };')
        db_session.commit()

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    return render_template("update-method.html",
                           title="Update a Method | Pitt Digital Scholarship Database",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           method=method,
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
    
    detach_person_area(person.public_id, area.area_name)
    
    db_session.execute(f'DELETE FROM person_area \
                        WHERE fk_person_id = { person.person_id }\
                        AND fk_area_id = { area.area_id };')
    db_session.commit()
    
    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))


@views_bp.route('/delete-person-unit/<person_id>/<unit_name>', methods=['GET', 'POST'])
@login_required
def delete_person_unit(person_id, unit_name):
    if current_user.is_authenticated:
        current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
               category="error")
        return redirect(url_for('auth_bp.login'))
    
    person = Person.query.filter_by(person_id=person_id).first()
    unit_name_list = unit_name.split(', ')
    unit = None
    subunit = None
    if len(unit_name_list) > 1:
        # Get unit information
        cur_subunit_name = unit_name_list[0]
        cur_unit_name = unit_name_list[1]
        subunit = Subunit.query.filter_by(subunit_name=cur_subunit_name).first()
        unit = Unit.query.filter_by(unit_name=cur_unit_name).first()

        # Delete person-subunit relation
        db_session.execute(f'DELETE FROM person_subunit \
                        WHERE fk_person_id = { person_id }\
                        AND fk_subunit_id = { subunit.subunit_id };')
        # Delete person-unit relation
        db_session.execute(f'DELETE FROM person_unit \
                        WHERE fk_person_id = { person_id }\
                        AND fk_unit_id = { unit.unit_id };')
    else:
        # Get unit information
        cur_unit_name = unit_name_list[0]
        unit = Unit.query.filter_by(unit_name=cur_unit_name)

        # Delete person-unit relation
        db_session.execute(f'DELETE FROM person_unit \
                        WHERE fk_person_id = { person_id }\
                        AND fk_unit_id = { unit.unit_id };')
        
    db_session.commit()

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


"""Functions to Show View Pages"""

@views_bp.route('/view-person/<public_id>', methods=['GET', 'POST'])
def view_person(public_id):
    # Get person record
    person = db_session.query(Person).filter_by(public_id=public_id).first()
    
    # Notify if person was not found in the DB and redirect to homepage
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
              category="error")
        return render_template("index.html",
                           title="Pitt Digital Scholarship Database",
                           user=current_user)
    
    # Check if current user can update and/or delete person record
    user_can_update = user_can_delete = False

    if not current_user.is_anonymous and current_user.is_authenticated:
        current_user.set_permissions()
    
        if current_user.permission_level == 4:
            user_can_update = user_can_delete = True
        elif person.added_by == current_user.user_id:
            user_can_update = True
    
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
    person_address = {}
    if person_address_result:
        address_items = ['building_name', 'room_number', 'street_address', 
                    'address_2', 'address_3', 'city', 'state', 'zipcode', 'campus']
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
