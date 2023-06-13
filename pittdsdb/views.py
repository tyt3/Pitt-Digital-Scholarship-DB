"""Module for Views"""
from flask import Blueprint, render_template, redirect, request, session, \
    flash, url_for, abort
from flask_login import login_required, current_user
from flask_session import Session
from flask_mail import Mail, Message
from git import Repo
import json
from .config import SECRET_KEY
from .database import db_session
from .models import *
from .add import *
from .get import *
from .search import *
from .update import *
from .delete import *
from .stored_procedures import *
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
                           title="Home",
                           user=current_user)

"""Function to Show About Page"""
@views_bp.route('/about')
def about():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("about.html", 
                           title="About",
                           user=current_user)


"""Function to Show Documentation Page"""
@views_bp.route('/documentation')
def documentation():
    if current_user.is_authenticated:
        current_user.set_permissions()

    return render_template("documentation.html",
                           title="Documentation",
                           user=current_user)


"""Function to Show Contact Page"""
@views_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    if request.method == "POST":
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg = Message(subject, sender='pittdsdb@gmail.com', recipients=['tyt3@pitt.edu'])
        msg.body = f"From: {full_name} <{email}> {message}" 
        mail.send(msg)

        return redirect(url_for('views_bp.index'))
    
    return render_template("contact.html",
                           title="Contact Us",
                           user=current_user)
    
    
"""Functions to Show Search Pages"""
@views_bp.route('/search')
def search():
    if current_user.is_authenticated:
        current_user.set_permissions()
    return render_template("search.html",
                           title="Search",
                           user=current_user)


@views_bp.route('/search-people', methods=['GET', 'POST'])
def search_people():
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    search = False
    search_results = None

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        title = request.form.get('title')
        support_types = request.form.getlist('support_type')
        campuses = request.form.getlist('campus')
        areas = request.form.getlist('supported_area')
        methods = request.form.getlist('supported_method')
        tools = request.form.getlist('supported_tool')
        tool_types = request.form.getlist('supported_tool_type')

        search_results = search_person(first_name, last_name, title, support_types, 
        campuses, areas, methods, tools, tool_types)[1]

        search = True
    
    return render_template("search-people.html",
                           title="Search People",
                           user=current_user,
                           existing=existing,
                           search_results=search_results,
                           search=search)


@views_bp.route('/search-units', methods=['GET', 'POST'])
def search_units():
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    search = False
    search_results = None

    if request.method == "POST":
        unit_name = request.form.get('unit_name')
        unit_types = request.form.getlist('unit_type')
        campuses = request.form.getlist('campus')
        areas = request.form.getlist('supported_area')
        resource_types = request.form.getlist('supported_resource_type')
        offers_funding = request.form.get('offers_funding')

        search_results = search_unit(unit_name, unit_types, campuses, 
                                     areas, resource_types, offers_funding)[1]

        search = True
    
    return render_template("search-units.html",
                           title="Search Units",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           search_results=search_results,
                           search=search)


@views_bp.route('/search-funding', methods=['GET', 'POST'])
def search_fundings():
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    search = False
    search_results = None

    if request.method == "POST":
        funding_name = request.form.get('funding_name')
        funding_types = request.form.getlist('funding_types')
        durations = request.form.getlist('duration')
        frequencies = request.form.getlist('frequency')
        payment_types = request.form.getlist('payment_type')
        min_amount = request.form.get('min_amount')
        max_amount = request.form.get('max_amount')
        career_levels = request.form.getlist('career_level')
        campuses = request.form.getlist('campus')

        search_results = search_funding(funding_name, funding_types, durations, 
                                     frequencies, payment_types, min_amount, 
                                     max_amount, career_levels, campuses)[1]

        search = True

    return render_template("search-funding.html",
                           title="Search Funding Opportunities",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           search_results=search_results,
                           search=search)


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
        affiliations = request.form.getlist('affiliation')
        email = request.form.get('email')
        web_address = request.form.get('web_address')
        phone = request.form.get('phone')
        scheduler_address = request.form.get('scheduler')
        other_contact = request.form.get('other_contact')
        preferred_contact = request.form.get('preferred_contact') 
        support_type = request.form.get('support_type')
        bio = request.form.get('bio')
        notes = request.form.get('notes')
        photo_url = request.form.get('photo_url')

        person = Person.query.filter_by(public_id=public_id).first()

        if person:
            if current_user.is_authenticated:
                current_user.set_permissions(person)

            if not current_user.can_update:
                flash("Your account does not have permission to update this person record.",
                      category="error")
                
                return redirect(url_for('views_bp.view_person', 
                                        public_id=public_id))

            update_person(person, first_name, last_name, pronouns, title, email, 
                          phone, scheduler_address, other_contact, 
                          preferred_contact, web_address, support_type, bio, 
                          notes, photo_url)

            # Update affiliations
            update_affiliations(person.person_id, person.first_name + ' ' + 
                                person.last_name, affiliations)

            # Commit changes
            db_session.commit()

            # Update graph node
            update_person_node(first_name + ' ' + last_name, public_id)

            return redirect(url_for('views_bp.view_person',
                                    public_id=person.public_id))
        else:
            if public_id != 'new':
                flash("404: Not Found. That person does not exist in the database.",
                      category="error")
                
                return redirect(url_for('views_bp.add_person',
                                        public_id='new'))

            new_person = add_person_to_db(first_name, last_name, title, pronouns, 
                                          email, phone, scheduler_address, 
                                          other_contact, preferred_contact,
                                          web_address, support_type, bio, notes, 
                                          photo_url, current_user.user_id)
                                            
            # Check if the person was added succesfully
            if new_person:
                if new_person[0]:
                    # Get person object
                    p = new_person[1]
                    person_id = p.person_id
                    public_id = p.public_id

                    # Add affiliation
                    for a in affiliations:
                        add_person_affiliation(person_id, a)


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
                           title="Add a Person",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           public_id=public_id)


@views_bp.route('/add-person-unit/<public_id>', 
                methods=['POST'])
@login_required
def add_person_unit(public_id):
    person = Person.query.filter_by(public_id=public_id).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions(person)

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_update:
        flash("Your account does not have permission to update this record.",
               category="error")
        
        return redirect(url_for('views_bp.view_person', 
                                        public_id=public_id))
    
    if request.method == "POST":
        # Get data from form and submit to database
        unit_name = request.form.get('unit_name')
        parent_unit_names = request.form.getlist('parent_unit_name')

        # Add unit(s)
        add_person_unit_to_db(person.person_id, 
                            person.first_name + " " + person.last_name,
                            unit_name)
        if parent_unit_names:
            for parent_unit in parent_unit_names:
                unit_subunit_match = check_unit_subunit(unit_name, parent_unit)
                
                if not unit_subunit_match:
                    flash("The selected unit is not associated with the selected \
                        parent unit.", category="error")
            
                    return redirect(url_for('views_bp.view_person',
                                            public_id=public_id))

                add_person_unit_to_db(person.person_id, person.first_name + " " + 
                                  person.last_name, parent_unit)

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    

@views_bp.route('/add-unit/<public_id>', methods=['GET', 'POST'])
@login_required
def add_unit(public_id):
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions()

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.", category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get all units
    unit = None
    units = get_all_units()
    unit_names = sorted(set([ res[0] for res in units]))

    # Get data from form and submit to database
    if request.method == "POST":
        unit_name = request.form.get('unit_name')
        unit_type = request.form.get('unit_type')
        parent_units = request.form.getlist('parent_unit')
        email = request.form.get('email')
        phone = request.form.get('phone')
        other_contact = request.form.get('other_contact')
        preferred_contact = request.form.get('preferred_contact')
        web_address = request.form.get('web_address')
        description = request.form.get('description')

        # Query for unit
        unit = Unit.query.filter_by(public_id=public_id).first()

        # If unit exists, update
        if unit:
            if current_user.is_authenticated:
                current_user.set_permissions(unit)
            
            if not current_user.can_update:
                flash("Your account does not have permission to update this unit record.", 
                      category="error")
                return redirect(url_for('auth_bp.login'))

            update_unit(unit, unit_name, unit_type, email, phone, other_contact,
                        preferred_contact, web_address, description)
            
            if parent_units:
                for parent_unit in parent_units:
                        cur_parent_unit = get_unit_by_name(parent_unit)
                        add_unit_subunit(unit, cur_parent_unit)
                        update_subunit_node(unit_name, public_id, parent_unit)
            else:
                update_unit_node(unit_name, public_id)

            # Delete any units not in list
            unit_parent_units = get_unit_subunits("subunit", public_id)

            for parent_unit in unit_parent_units:
                if parent_unit['parent_unit_name'] not in parent_units:
                    cur_unit = get_unit_by_name(parent_unit['parent_unit_name'])
                    delete_unit_subunit(unit, cur_unit)

            return redirect(url_for('views_bp.view_unit',
                                    public_id=unit.public_id))
        
        # If unit does not exist, add it 
        else:
            success, new_unit = add_unit_to_db(unit_name=unit_name,
                                                unit_type=unit_type,
                                                email=email, 
                                                web_address=web_address,
                                                phone=phone,
                                                other_contact=other_contact,
                                                preferred_contact=preferred_contact,
                                                description=description,
                                                added_by=current_user.get_id())
            if success:
                # Update public id
                public_id = new_unit.public_id
                                
                if parent_units:                   
                    # Add unit-subunit relations
                    for parent_unit in parent_units:
                        cur_parent_unit = get_unit_by_name(parent_unit)
                        add_unit_subunit(new_unit, cur_parent_unit)
                        add_subunit_node(unit_name, public_id, parent_unit)
                        attach_unit_subunit(cur_parent_unit.public_id, public_id)
                else:
                    # Add unit node
                    add_unit_node(unit_name, public_id)

                return redirect(url_for('views_bp.view_unit', public_id=public_id))
            else:
                return redirect(url_for('views_bp.add_unit', public_id=public_id))
        
    return render_template("/add-unit.html",
                           title="Add a Unit",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           unit=unit,
                           unit_names=unit_names,
                           public_id=public_id)


@views_bp.route('/add-funding/<public_id>', methods=['GET', 'POST'])
@login_required
def add_funding(public_id): # Change so that it asks for funding public id
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
        funding_name = request.form.get('funding_name')
        funding_type = request.form.get('funding_type')
        duration = request.form.get('duration')
        frequency = request.form.get('frequency')
        payment_type = request.form.get('payment_type')
        payment_amount = request.form.get('payment_amount')
        career_level = request.form.get('career_level')
        web_address = request.form.get('website')
        notes = request.form.get('notes')
        campus = request.form.get('campus')

        funding = Funding.query.filter_by(funding_name=funding_name).first()

        if funding:
            flash("That funding record already exists!", category="error")
            return redirect(url_for('views_bp.view_funding', 
                                    public_id=funding.public_id))

        else:
            new_funding = add_funding_to_db(funding_name=funding_name, 
                                            funding_type=funding_type,
                                            duration=duration, 
                                            frequency=frequency, 
                                            payment_type=payment_type,
                                            payment_amount=payment_amount,
                                            career_level=career_level,
                                            web_address=web_address, 
                                            notes=notes,
                                            campus=campus,
                                            added_by=current_user.user_id)[1]
            
            if new_funding:
                if public_id not in ['None', 'new']:
                    unit = Unit.query.filter_by(public_id=public_id).first()
                    if not unit:
                        flash("404: Not Found. That unit does not exist in the database.",
                                category="error")
                        return redirect(url_for('views_bp.index'))
                    
                    # Check if user can update record
                    if current_user.is_authenticated:
                        current_user.set_permissions(unit)
                    if not current_user.can_update:
                        flash("Your account does not have permission to update this unit record.",
                            category="error")
                        return redirect(url_for('views_bp.view_unit',
                                                public_id=unit.public_id))
                    
                    add_funding_unit_to_db(new_funding.funding_id,
                                           new_funding.funding_name,
                                           unit.unit_name)

                return redirect(url_for('views_bp.view_funding', 
                                        public_id=new_funding.public_id))
            else:
                flash('The funding record was not added. Please try again.', 
                      category='error')
                return redirect(url_for('views_bp.add_funding', 
                                        public_id=public_id))
    
    return render_template("/add-funding.html",
                           title="Add a Funding Opportunity",
                           user=current_user,
                           vocab=vocab,
                           existing=existing)


@views_bp.route('/add-parent-unit/<unit_public_id>/<parent_unit_public_id>', methods=['POST'])
@login_required
def add_parent_unit(unit_public_id, parent_unit_public_id):
    unit, is_subunit = get_unit(unit_public_id)
    parent_unit = Unit.query.filter_by(public_id=parent_unit_public_id).first()

    if current_user.is_authenticated:
        current_user.set_permissions(unit)
    
    if not current_user.can_update:
        flash("Your account does not have permission to update this unit record.",
               category="error")
        
        return redirect(url_for('auth_bp.login'))
    
    # Add unit-subunit relationship
    add_unit_subunit(unit, parent_unit)
            
    # add neo4j code
    
    return redirect(url_for('views_bp.view_unit',
                            public_id=unit.public_id))


@views_bp.route('/add-funding-unit/<public_id>', 
                methods=['POST'])
@login_required
def add_funding_unit(public_id):
    funding = Funding.query.filter_by(public_id=public_id).first()
    
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions(funding)

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_update:
        flash("Your account does not have permission to update this record.",
               category="error")
        
        return redirect(url_for('views_bp.view_funding', 
                                        public_id=public_id))
    
    if request.method == "POST":
        # Get data from form and submit to database
        unit_name = request.form.get('unit_name')
        parent_unit_name = request.form.get('parent_unit_name')

        # Add unit(s)
        if parent_unit_name == "None":
            add_funding_unit_to_db(funding.funding_id, funding.funding_name,
                                   unit_name)
        else:
            unit_subunit_match = check_unit_subunit(unit_name, parent_unit_name)
            
            if not unit_subunit_match:
                flash("The selected unit is not associated with the selected \
                       parent unit.", category="error")
        
                return redirect(url_for('views_bp.view_funding',
                                        public_id=public_id))

            add_funding_unit_to_db(funding.funding_id, funding.funding_name,
                                   unit_name)

        return redirect(url_for('views_bp.view_funding',
                                public_id=funding.public_id))


@views_bp.route('/add-address/<entity_type>/<public_id>', methods=['POST'])
@login_required
def add_address(entity_type, public_id):    
    address = entity = entity_id = entity_name = None
    if entity_type == 'person':
        entity = Person.query.filter_by(public_id=public_id).first()
        entity_id = entity.person_id
        entity_name = entity.first_name + " " + entity.last_name
    elif entity_type == 'unit':
        entity = Unit.query.filter_by(public_id=public_id).first()
        entity_id = entity.unit_id
        entity_name = entity.unit_name
    
    if current_user.is_authenticated:
        current_user.set_permissions(entity)
    
    if not current_user.can_update:
        flash("Your account does not have permission to update this record",
               category="error")
    else:
        building_name = request.form.get('building')
        room_number = request.form.get('office')
        street_address = request.form.get('street_address')
        address_2 = request.form.get('address_2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        campus = request.form.get('campus')

        exists, address = get_address(building_name=building_name, 
                                      room_number=room_number,
                                      street_address=street_address, 
                                      address_2=address_2, city=city, 
                                      state=state, zipcode=zipcode, 
                                      campus=campus)
        if not exists:
            # Add new address
            success, address = add_address_to_db(building_name=building_name, 
                                                room_number=room_number,
                                                street_address=street_address,
                                                address_2=address_2, 
                                                city=city, state=state, 
                                                zipcode=zipcode, campus=campus)

        # Add entity_address relationship
        add_entity_address(entity_id, entity_name, entity_type, 
                           address.address_id)
            
    if entity_type == 'person':
        return redirect(url_for('views_bp.view_person',
                                public_id=entity.public_id))
    else:
        return redirect(url_for('views_bp.view_unit',
                                public_id=entity.public_id)) 


@views_bp.route('/add-area/<public_id>', methods=['POST'])
@login_required
def add_area(public_id):
    # Get object information
    person = Person.query.filter_by(public_id=public_id).first()

    if current_user.is_authenticated:
        current_user.set_permissions(person)
    if not current_user.can_update:
        flash("Your account does not have permission to update this record",
               category="error")
    
    # Get form values
    area_name = request.form.get('area')
    new_area_name = request.form.get('new_area')
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    if new_area_name:
        existing_area = Area.query.filter_by(area_name=new_area_name).first()

        if existing_area:
            flash("That area already exists!", category='error')
        else:
            # Add Area node
            # add_area_node(new_area_name)
            area_name = new_area_name

    result = manage_person_area('add', current_user.user_id, person.person_id, 
                                 area_name, '', proficiency_level, notes)

    #attach_person_area(public_id, area_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-method/<public_id>', methods=['POST'])
@login_required
def add_method(public_id):
    # Get object information
    person = Person.query.filter_by(public_id=public_id).first()

    # Check if user can update record
    current_user.set_permissions(person)
    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    # Get form values
    area_names = request.form.getlist('area')
    method_name = request.form.get('method')
    new_method_name = request.form.get('new_method')
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    # Add method and relations
    if new_method_name:
        # Make sure the method name being added doesn't already exist
        existing_method = Method.query.filter_by(method_name=new_method_name).first()
        if existing_method:
            method_name = existing_method
        else:
            method_name = new_method_name
    
    # Add person-support relationships
    for area_name in area_names:
        manage_person_method('add', current_user.user_id, person.person_id, 
                              area_name, method_name, None, proficiency_level,
                              notes)
        
        # Add relations in neo4j
        result = get_relations("Person", "public_id", person.public_id, "Area", "name", area_name)
        if len(result) == 0:
            attach_person_area(person.public_id, area_name)
        result = get_relations("Person", "public_id", person.public_id, "Method", "name", method_name)
        if len(result) == 0:
            attach_person_method(person.public_id, method_name)
        result = get_relations("Area", "name", area_name, "Method", "name", method_name)
        if len(result) == 0:
            attach_area_method(area_name, method_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-tool/<public_id>', methods=['POST'])
@login_required
def add_tool(public_id):
    # Get object information
    person = Person.query.filter_by(public_id=public_id).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update record
    if current_user.is_authenticated:
        current_user.set_permissions(person)
    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    # Get form values
    area_names = request.form.getlist('area')
    method_names = request.form.getlist('method')
    tool_name = request.form.get('tool')
    new_tool_name = request.form.get('new_tool')
    tool_type = request.form.get('tool_type')
    web_address = request.form.get('web_address')
    proficiency_level = request.form.get('proficiency')
    notes = request.form.get('notes')

    # Check if new_tool_name was input in form
    if new_tool_name:
        # Make sure the tool name being added doesn't already exist
        existing_tool = Tool.query.filter_by(tool_name=new_tool_name).first()
        if existing_tool:
            tool_name = existing_tool.name
        else:
            tool_name = new_tool_name
    
    # Add person-support relationships
    for area_name in area_names:
        for method_name in method_names:
            manage_person_tool('add', current_user.user_id, person.person_id,
                                area_name, method_name, tool_name, tool_type,
                                web_address, None, proficiency_level, notes)

            result = get_relations("Person", "name", person.public_id, "Area", "name", area_name)
            if len(result) == 0:
                attach_person_area(person.public_id, area_name)
            result = get_relations("Person", "name", person.public_id, "Method", "name", method_name)
            if len(result) == 0:
                attach_person_method(person.public_id, method_name)
            result = get_relations("Person", "name", person.public_id, "Tool", "name", tool_name)
            if len(result) == 0:
                attach_person_tool(person.public_id, tool_name)

            # attach area to method if not exists
            result = get_relations("Area", "name", area_name, "Method", "name", method_name)
            if len(result) == 0:
                attach_area_method(area_name, method_name)
            # attach tool to method if not exists
            result = get_relations("Tool", "name", tool_name, "Method", "name", method_name)
            if len(result) == 0:
                attach_tool_method(tool_name, method_name)
            # attach tool to area if not exists
            result = get_relations("Area", "name", area_name, "Tool", "name", tool_name)
            if len(result) == 0:
                attach_area_tool(area_name, tool_name)

    return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))


@views_bp.route('/add-resource/<public_id>', methods=['POST'])
@login_required
def add_resource(public_id):
    current_user.set_permissions()
    if not current_user.can_add:
        flash("Your account does not have permission to add to the database.",
            category="error")
        return redirect(url_for('views_bp.index'))

     # Get object information
    unit, is_subunit = get_unit(public_id)
    resource = None

    if public_id not in ['new', 'None']:
        if not unit:
            flash("404: Not Found. That unit does not exist in the database.",
                    category="error")
            return redirect(url_for('views_bp.index'))
    
        # Check if user can update record
        if current_user.is_authenticated:
            current_user.set_permissions(unit)
        if not current_user.can_update:
            flash("Your account does not have permission to update this unit record.",
                category="error")
            return redirect(url_for('views_bp.view_unit',
                                    public_id=unit.public_id))
    
    # Get form values
    areas = request.form.getlist('area')
    new_areas = request.form.get('new_area')
    resource_name = request.form.get('resource')
    new_resource = request.form.get('new_resource')
    resource_type = request.form.get('resource_type')
    web_address = request.form.get('web_address')
    notes = request.form.get('notes')

    if new_areas:
        new_areas = re.sub(r',\s*', ',', request.form.get('new_area')).split(',')

        for area in new_areas:
            existing_area = Area.query.filter_by(area_name=area).first()
            if not existing_area:
                add_area_to_db(area)
    else:
        new_areas = []

    if not areas and not new_areas:
        session['resource_form'] = {'alerted': 0,
                                    'resource_name': resource_name,
                                    'new_resource': new_resource,
                                    'resource_type': resource_type,
                                    'web_address': web_address,
                                    'notes': notes}

        flash("Please choose an existing area or enter a new area.", 
              category="modal-form-error")
        
        return redirect(url_for('views_bp.view_unit',
                                public_id=public_id))

    # Add resource and relations
    if new_resource:
        # Make sure the resource name being added doesn't already exist
        existing_resource = Resource.query.filter_by(resource_name=new_resource).first()
        if existing_resource:
            resource = existing_resource
        else:
            success, resource = add_resource_to_db(new_resource, resource_type,
                                                   web_address)
    else:
        resource = Resource.query.filter_by(resource_name=resource_name).first()

    # Add resource-area relations     
    add_resource_area(resource.resource_id, resource.resource_name, 
                    areas + new_areas)
    
    # Add unit-resource relations
    if unit:
        add_unit_resource(unit.unit_id, unit.unit_name, resource.resource_id, 
                        resource.resource_name, areas + new_areas, notes)
        
        # Delete resource-area relations not in given list
        delete_entity_area(unit.unit_id, "resource", resource.resource_id, 
                        resource_name, areas + new_areas)
    
    return redirect(url_for('views_bp.view_unit',
                                public_id=public_id))


"""Functions to Show Update Pages"""

@views_bp.route('/update-address/<entity_type>/<public_id>/<address_id>/', methods=['GET', 'POST'])
@login_required
def update_entity_address(entity_type, public_id, address_id):
    # Get entity
    entity = entity_id = entity_name = None
    if entity_type == "person":
        entity = Person.query.filter_by(public_id=public_id).first()
        entity_id = entity.person_id
        entity_name = entity.first_name + " " + entity.last_name
    elif entity_type == "unit":
        entity = Unit.query.filter_by(public_id=public_id).first()
        entity_id = entity.unit_id
        entity_name = entity.unit_name
    
    if not entity:
        flash(f"404: Not Found. That { entity_type } does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if user can update record
    if current_user.is_authenticated:
        current_user.set_permissions(entity)

    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for(f'views_bp.view_{entity_type}',
                                public_id=entity.public_id))
    
    # Get address
    address = Address.query.filter_by(address_id=address_id).first()

    if not address and address != 'new':
        flash("404: Not Found. That address does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    if request.method == "POST":
        building_name = request.form.get('building')
        room_number = request.form.get('office')
        street_address = request.form.get('street_address')
        address_2 = request.form.get('address_2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        campus = request.form.get('campus')

        update_address(entity_type, entity_id, entity.public_id,
                       entity_name, address, building_name, room_number, 
                       street_address, address_2, city, state, zipcode, campus)
        
        if entity_type == "person":
            return redirect(url_for('views_bp.view_person',
                                public_id=entity.public_id))
        elif entity_type == "unit":
            return redirect(url_for('views_bp.view_unit',
                                public_id=entity.public_id)) 

    return render_template("update-address.html",
                           title="Update an Address",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           entity=entity,
                           entity_type=entity_type,
                           address=address)


@views_bp.route('/update-area/<area_name>/<public_id>', methods=['GET', 'POST'])
@login_required
def update_area(area_name, public_id):
    # Get object information
    person = Person.query.filter_by(public_id=public_id).first()
    area = Area.query.filter_by(area_name=area_name).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update person record
    if current_user.is_authenticated:
        current_user.set_permissions(person)
    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    if not area:
        flash("404: Not Found. That area does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(area)

    # Get person-area information
    proficiency_id = get_person_relations(person.person_id, person.public_id, 
                                 "fk_proficiency_id", "area",
                                 area.area_id)[0]
    proficiency = Proficiency.query.filter_by(proficiency_id=proficiency_id).first()
    notes = get_person_relations(person.person_id, person.public_id, 
                                 "notes", "area",
                                 area.area_id)[0]
    
    if request.method == "POST":
        updated_proficiency = request.form.get('proficiency')
        updated_notes = request.form.get('notes')
        result = manage_person_area('update', current_user.user_id, 
                                     person.person_id, area.area_name, None,
                                     updated_proficiency, updated_notes)
        

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    return render_template("update-area.html",
                           title="Update an Area",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           area=area,
                           proficiency=proficiency,
                           notes=notes)


@views_bp.route('/update-method/<method_name>/<public_id>', methods=['GET', 'POST'])
@login_required
def update_method(method_name, public_id):
    person = Person.query.filter_by(public_id=public_id).first()
    method = Method.query.filter_by(method_name=method_name).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(person)

    if not current_user.can_update:
        flash("Your account does not have permission to update this record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    if not method:
        flash("404: Not Found. That method does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(method)
    
    if request.method == "GET":
        areas = get_field_list(f"SELECT DISTINCT area_name FROM vw_person_support \
                                WHERE method_name = '{method_name}'")

        proficiency_id = get_person_relations(person.person_id, person.public_id, 
                                    "fk_proficiency_id", "method", 
                                    method.method_id)[0]
        proficiency = Proficiency.query.filter_by(proficiency_id=proficiency_id).first()
        notes = get_person_relations(person.person_id, person.public_id,  
                                    "notes", "method",
                                    method.method_id)[0]
    
    if request.method == "POST":
        areas = request.form.getlist('area')
        updated_name = request.form.get('new_name')
        updated_proficiency = request.form.get('proficiency')
        updated_notes = request.form.get('notes')

        for area in areas:
            manage_person_method('update', current_user.user_id, 
                                  person.person_id, area, method_name, 
                                  updated_name, updated_proficiency, 
                                  updated_notes)
            
        # Add in neo4j code

        # Delete any method-area relations that are no longer supported
        delete_entity_area(person.person_id, "method", method.method_id, 
                           method.method_name, areas)

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    return render_template("update-method.html",
                           title="Update a Method",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           areas=areas,
                           method=method,
                           proficiency=proficiency,
                           notes=notes)


@views_bp.route('/update-tool/<tool_name>/<public_id>', methods=['GET', 'POST'])
@login_required
def update_tool(tool_name, public_id):
    person = Person.query.filter_by(public_id=public_id).first()
    tool = Tool.query.filter_by(tool_name=tool_name).first()
    
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    if current_user.is_authenticated:
        current_user.set_permissions(person)

    if not current_user.can_update:
        flash("Your account does not have permission to update this record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    if not tool:
        flash("404: Not Found. That tool does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(tool)
    
    if request.method == "GET":
        areas = get_field_list(f"SELECT DISTINCT area_name FROM vw_person_support \
                                WHERE tool_name = '{tool_name}'")
        methods = get_field_list(f"SELECT DISTINCT method_name FROM vw_person_support \
                                WHERE tool_name = '{tool_name}'")
        proficiency_id = get_person_relations(person.person_id, person.public_id, 
                                    "fk_proficiency_id", "tool", 
                                    tool.tool_id)[0]
        proficiency = Proficiency.query.filter_by(proficiency_id=proficiency_id).first()
        notes = get_person_relations(person.person_id, person.public_id,  
                                    "notes", "tool",
                                    tool.tool_id)[0]
    
    if request.method == "POST":
        areas = request.form.getlist('area')
        methods = request.form.getlist('method')
        tool_type = request.form.get('tool_type')
        web_address = request.form.get('web_address')
        updated_name = request.form.get('new_name')
        updated_proficiency = request.form.get('proficiency')
        updated_notes = request.form.get('notes')

        for area in areas:
            for method in methods:
                manage_person_tool('update', current_user.user_id, 
                                    person.person_id, area, method, tool_name, 
                                    tool_type, web_address, updated_name, 
                                    updated_proficiency, updated_notes)    
                
        # Add in neo4j code

        # Delete any method-area relations that are no longer supported
        delete_entity_area(person.person_id, "tool", tool.tool_id, 
                           tool.tool_name, areas)
        
        # Delete any method-tool relations that are no longer supported
        delete_method_tool(person.person_id, tool.tool_id, tool.tool_name,
                           methods)

        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))

    return render_template("update-tool.html",
                           title="Update a Tool",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           person=person,
                           areas=areas,
                           methods=methods,
                           tool=tool,
                           proficiency=proficiency,
                           notes=notes)


@views_bp.route('/update-unding/<public_id>', methods=['POST'])
@login_required
def update_funding(public_id): # Change so that it asks for funding public id
    funding = Funding.query.filter_by(public_id=public_id).first()

    if not funding:
        flash("That funding does exist!", category="error")
        return redirect(url_for('views_bp.add_funding', public_id='new'))
    
    # Check if the user is logged in and, if so, set permissions
    if current_user.is_authenticated:
        current_user.set_permissions(funding)

    # Check if user can add to the database and, if not, redirect
    if not current_user.can_update:
        flash("Your account does not have permission to add to the database.", 
              category="error")
        return redirect(url_for('auth_bp.login'))
    
    # Get data from form and submit to database
    funding_name = request.form.get('funding_name')
    funding_type = request.form.get('funding_type')
    duration = request.form.get('duration')
    frequency = request.form.get('frequency')
    payment_type = request.form.get('payment_type')
    payment_amount = request.form.get('payment_amount')
    career_level = request.form.get('career_level')
    web_address = request.form.get('website')
    notes = request.form.get('notes')
    campus = request.form.get('campus')


    update_funding_in_db(funding, funding_name, funding_type, duration, 
                         frequency, payment_type, payment_amount, 
                         career_level, web_address, notes, campus)

    # Add neo4j

    return redirect(url_for('views_bp.view_funding',
                            public_id=public_id))


@views_bp.route('/update-resource/<resource_name>/<public_id>', methods=['GET', 'POST'])
@login_required
def update_resource(resource_name, public_id):
    unit, is_subunit = get_unit(public_id)
    resource = Resource.query.filter_by(resource_name=resource_name).first()
    notes = ""

    if not unit:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(unit)

    if not current_user.can_update:
        flash("Your account does not have permission to update this record.",
               category="error")
        return redirect(url_for('views_bp.view_unit',
                                public_id=unit.public_id))

    if not resource:
        flash("404: Not Found. That resource does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(resource)
    
    # View form
    if request.method == "GET":
        areas = get_field_list(f"SELECT DISTINCT area_name FROM vw_unit_support \
                                WHERE resource_name = '{resource_name}'\
                                AND fk_public_id = '{public_id}'")
        notes = get_field_list(f"SELECT resource_notes FROM vw_unit_support\
                                WHERE resource_name = '{resource_name}'\
                                AND fk_public_id = '{public_id}'")
    
    # Submit form
    if request.method == "POST":
        # Get form values
        areas = request.form.getlist('area')
        new_resource = request.form.get('new_resource')
        resource_type = request.form.get('resource_type')
        web_address = request.form.get('web_address')
        updated_notes = request.form.get('notes')

        # Update resource records
        update_unit_resource(unit.unit_id, unit.unit_name, resource, areas,
                                new_resource, resource_type, web_address, 
                                updated_notes)
            
        # Add in neo4j code

        return redirect(url_for('views_bp.view_unit',
                                public_id=unit.public_id))

    return render_template("update-resource.html",
                           title="Update a Resource",
                           user=current_user,
                           existing=existing,
                           vocab=vocab,
                           resource=resource,
                           unit=unit,
                           areas=areas,
                           notes=notes)


"""Functions to Delete Records"""

@views_bp.route('/delete-person/<public_id>', methods=['GET', 'POST'])
@login_required
def delete_person(public_id):
    person = Person.query.filter_by(public_id=public_id).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(person)

    if not current_user.can_delete:
        flash("Your account does not have permission to delete this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    # Delete person record
    delete_person_from_db(person)

    return redirect(url_for('views_bp.index'))


@views_bp.route('/delete-unit/<public_id>', methods=['GET', 'POST'])
@login_required
def delete_unit(public_id):
    unit, is_subunit = get_unit(public_id)

    if not unit:
        flash("404: Not Found. That unit does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(unit)

    if not current_user.can_delete:
        flash("Your account does not have permission to delete this unit record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=unit.public_id))
    
    # Delete unit record
    delete_unit_from_db(unit)

    return redirect(url_for('views_bp.index'))


@views_bp.route('/delete-funding/<public_id>', methods=['GET', 'POST'])
@login_required
def delete_funding(public_id):
    funding = Funding.query.filter_by(public_id=public_id).first()
    
    if not funding:
        flash("404: Not Found. That funding does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(funding)

    if not current_user.can_delete:
        flash("Your account does not have permission to delete this person record.",
               category="error")
        return redirect(url_for('views_bp.view_funding',
                                public_id=funding.public_id))
    
    # Delete funding record
    delete_funding_from_db(funding)

    return redirect(url_for('views_bp.index'))


@views_bp.route('/delete-unit/<person_id>/<unit_public_id>', methods=['GET', 'POST'])
@login_required
def delete_person_unit(person_id, unit_public_id):
    person = Person.query.filter_by(person_id=person_id).first()
    unit, is_subunit = get_unit(unit_public_id)

    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(person)
    
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    if not current_user.can_update:
        flash("Your account does not have permission to delete this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    delete_person_unit_from_db(person_id, unit.unit_id)

    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))


@views_bp.route('/delete-parent-unit/<unit_public_id>/<parent_unit_public_id>', methods=['POST'])
@login_required
def delete_parent_unit(unit_public_id, parent_unit_public_id):
    unit, is_subunit = get_unit(unit_public_id)
    parent_unit = Unit.query.filter_by(public_id=parent_unit_public_id).first()
    user_can_delete = False

    if current_user.is_authenticated:
        current_user.set_permissions()
        
        if current_user.permission_level == 4:
            user_can_delete = True
        elif unit.added_by == current_user.user_id:
            user_can_delete = True
    
    if not user_can_delete:
        flash("Your account does not have permission to delete from the database.",
               category="error")
        
        return redirect(url_for('auth_bp.login'))
    
    # Delete unit-subunit relationship
    delete_unit_subunit(unit, parent_unit)
            
    # add neo4j code
    
    return redirect(url_for('views_bp.view_unit',
                            public_id=unit.public_id))


@views_bp.route('/delete-funding-unit/<funding_id>/<unit_public_id>', methods=['GET', 'POST'])
@login_required
def delete_funding_unit(funding_id, unit_public_id):
    unit, is_subunit = get_unit(unit_public_id)
    funding = Funding.query.filter_by(funding_id=funding_id).first()

    if not unit:
        flash("404: Not Found. That unit not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    if not funding:
        flash("404: Not Found. That funding does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if user can update area record
    if current_user.is_authenticated:
        current_user.set_permissions(funding)

    if not current_user.can_update:
        flash("Your account does not have permission to delete this funding record.",
               category="error")
        return redirect(url_for('views_bp.view_funding',
                                public_id=funding.public_id))
    
    # Delete unit-funding relationship
    delete_unit_funding("unit", unit.unit_id, unit.unit_name, funding_id, 
                        funding.funding_name)
            
    # add neo4j code
    
    return redirect(url_for('views_bp.view_funding',
                            public_id=funding.public_id))


@views_bp.route('/delete-area/<area_id>/<person_id>', methods=['GET', 'POST'])
@login_required
def delete_area(area_id, person_id):
    person = Person.query.filter_by(person_id=person_id).first()
    area = Area.query.filter_by(area_id=area_id).first()

    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
    
    detach_person_area(person.public_id, area.area_name)

    result = manage_person_area('delete', current_user.user_id, 
                                     person.person_id, area.area_name, '',
                                     None, None)
    
    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))


@views_bp.route('/delete-method/<method_id>/<person_id>', methods=['GET', 'POST'])
@login_required
def delete_method(method_id, person_id):
    person = Person.query.filter_by(person_id=person_id).first()
    method = Method.query.filter_by(method_id=method_id).first()
    
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
        
    detach_person_method(person.public_id, method.method_name)

    result = manage_person_method('delete', current_user.user_id, person.person_id, 
                              None, method.method_name, None, None, None)
    
    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))


@views_bp.route('/delete-tool/<tool_id>/<person_id>', methods=['GET', 'POST'])
@login_required
def delete_tool(tool_id, person_id):
    person = Person.query.filter_by(person_id=person_id).first()
    tool = Tool.query.filter_by(tool_id=tool_id).first()
    
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    if not current_user.can_update:
        flash("Your account does not have permission to update this person record.",
               category="error")
        return redirect(url_for('views_bp.view_person',
                                public_id=person.public_id))
        
    detach_person_tool(person.public_id, tool.tool_name)

    result = manage_person_tool('delete', current_user.user_id, 
                                person.person_id, None, None, tool.tool_name, 
                                None, None, None, None, None)
    
    return redirect(url_for('views_bp.view_person',
                            public_id=person.public_id))


@views_bp.route('/delete-resource/<resource_id>/<public_id>', methods=['GET', 'POST'])
@login_required
def delete_resource(resource_id, public_id):
    unit, is_subunit = get_unit(public_id)
    resource = Resource.query.filter_by(resource_id=resource_id).first()
    
    if not unit:
        flash("404: Not Found. That unit does not exist in the database.",
                category="error")
        return redirect(url_for('views_bp.index'))

    if not current_user.can_update:
        flash("Your account does not have permission to update this unit record.",
               category="error")
        return redirect(url_for('views_bp.view_unit',
                                public_id=unit.public_id))
    
    # Delete resource
    delete_unit_resource(unit.unit_id, unit.unit_name, resource_id,
                         resource.resource_name)
            
    # add neo4j code
    
    return redirect(url_for('views_bp.view_unit',
                            public_id=unit.public_id))


"""Functions to Show View Pages"""

@views_bp.route('/view-person/<public_id>', methods=['GET', 'POST'])
def view_person(public_id):
    # Get person record
    person = db_session.query(Person).filter_by(public_id=public_id).first()
    
    # Notify if person was not found in the DB and redirect to homepage
    if not person:
        flash("404: Not Found. That person does not exist in the database.",
              category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if current user can update and/or delete person recor
    if current_user.is_authenticated:
        current_user.set_permissions(person)
    
    # get person support information
    person_support = get_person_support(person.person_id)
        
    # Get affiliation(s)
    affiliations = get_person_relations(person.person_id, person.public_id, 
                                               "affiliation_type",
                                               "affiliation")
    
    # Get Unit information
    units = get_person_units('person', person.public_id)

    # Get address
    addresses = get_entity_address(public_id)

    # Get rendered text from Markdown-enabled fields
    other_contact = get_markdown(person.other_contact)
    bio = get_markdown(person.bio)
    notes = get_markdown(person.notes)

    return render_template("view-person.html",
                           title="View a Person",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           person=person,
                           units=units,
                           affiliations=affiliations,
                           addresses=addresses,
                           person_support=person_support,
                           other_contact=other_contact,
                           bio=bio,
                           notes=notes)


@views_bp.route('/view-unit/<public_id>', methods=['GET', 'POST'])
def view_unit(public_id):
    # Get unit record and information
    unit, is_subunit = get_unit(public_id)

    # Notify if unit was not found in the DB and redirect to homepage
    if not unit:
        flash("404: Not Found. That unit does not exist in the database.",
              category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if current user can update and/or delete person recor
    if current_user.is_authenticated:
        current_user.set_permissions(unit)
    
    # Get unit relationships
    parent_units = subunits = []
    parent_unit_names = []
    if is_subunit:
        # Get parent units
        parent_units = get_unit_subunits("subunit", public_id)
        parent_unit_names = sorted(set(
            [ res['parent_unit_name']
             for res in parent_units if res['parent_unit_name'] ]))

        # Get subunits
        subunits = get_unit_subunits("unit", public_id)
    else:
        # Get subunits
        subunits = get_unit_subunits("unit", public_id)

    # Get people
    people = get_person_units("unit", public_id)

    # Get address(es)
    addresses = get_entity_address(public_id)

    # Get areas
    areas_results = get_unit_support("area", public_id)
    areas = sorted(set([ res['area_name'] for res in areas_results ]))

    # Get resources
    resource_results = get_unit_support("resource", public_id)
    resources = []
    resource_names = []

    for res in resource_results:
        resource = res['resource_name']
        type = res['resource_type']
        website = res['resource_website']
        notes = res['resource_notes']

        if resource not in resource_names:
            resources.append({'name': resource, 'type': type, 
                              'website': website, 'notes': notes})
            resource_names.append(resource)

    # Get funding oppportunities
    funding = get_unit_funding("unit", public_id)

    # Get rendered text from Markdown-enabled fields
    other_contact = get_markdown(unit.other_contact)
    description = get_markdown(unit.description)

    # Handle form information on session
    if 'resource_form' in session:
        session['resource_form']['alerted'] += 1
        if session['resource_form']['alerted'] > 1:
            session.pop('resource_form', None)

    return render_template("view-unit.html",
                           title="View a Unit",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           unit=unit,
                           is_subunit=is_subunit,
                           addresses=addresses,
                           parent_units=parent_units,
                           parent_unit_names=parent_unit_names,
                           subunits=subunits,
                           people=people,
                           areas=areas,
                           resources=resources,
                           resource_names=resource_names,
                           funding=funding,
                           other_contact=other_contact,
                           description=description)


@views_bp.route('/view-funding/<public_id>', methods=['GET', 'POST'])
def view_funding(public_id):
    # Get person record
    funding = Funding.query.filter_by(public_id=public_id).first()
    
    # Notify if person was not found in the DB and redirect to homepage
    if not funding:
        flash("404: Not Found. That funding does not exist in the database.",
              category="error")
        return redirect(url_for('views_bp.index'))
    
    # Check if current user can update and/or delete person recor
    if current_user.is_authenticated:
        current_user.set_permissions(funding)
    
    # Get unit information
    units = get_unit_funding('funding', public_id)
    unit_names = [ res['unit_name'] for res in units if res['unit_name'] ]

    # Get campuses
    campuses = sorted(set([ res['campus'] for res in units if res['campus'] ]))

    # Get rendered text from Markdown-enabled fields
    #description = get_markdown(funding.description)
    notes = get_markdown(funding.notes)
        
    return render_template("view-funding.html",
                           title="View a Funding Opportunity",
                           user=current_user,
                           vocab=vocab,
                           existing=existing,
                           funding=funding,
                           units=units,
                           unit_names=unit_names,
                           campuses=campuses,
                           #description=description,
                           notes=notes)


@views_bp.route('/test/<username>', methods=['GET', 'POST'])
def test(username):
    if current_user.is_authenticated:
        current_user.set_permissions()
    
    user = User.query.filter_by(user_name=username).first()
    user_name = str(user.first_name) + " " + str(user.last_name)

    # delete_entity_area("method", 1, "Topic Modeling", [2], "Text Mining & Analysis")
    
    return render_template("test.html",
                           title="Test",
                           user=current_user,
                           user_name=user_name,
                           vocab=vocab,
                           existing=existing)


@views_bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method != 'POST':
        return 'OK'
    else:
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)
        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)
        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)
        if not request.is_json:
            abort(abort_code)
        if 'User-Agent' not in request.headers:
            abort(abort_code)
        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)

        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not verify_signature(x_hub_signature, request.data, SECRET_KEY):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/master':
            return json.dumps({'msg': 'Not master; ignoring'})

        repo = Repo('https://github.com/tyt3/Pitt-Digital-Scholarship-DB')
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')

        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)
