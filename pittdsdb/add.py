from flask import Blueprint, request, jsonify, flash
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from flask_restful import Api, Resource
from functools import wraps
from .database import db_session, engine
from .models import *
from .schemas import *
from .get import *
from .utilities import *


""" Person Functions """

def add_person_to_db(first_name, last_name, title, pronouns, email, phone, 
                     scheduler_address, other_contact, preferred_contact,
                     web_address, support_type, bio, notes, photo_url, added_by):
    person = None

    try:
        # Create new person object
        new_person = Person(first_name = first_name,
                            last_name = last_name,
                            title = title,
                            pronouns = pronouns,
                            email = email,
                            web_address = web_address,
                            phone = phone,
                            scheduler_address = scheduler_address,
                            preferred_contact = preferred_contact,
                            other_contact = other_contact,
                            support_type = support_type,
                            bio = bio,
                            added_by = added_by,
                            notes = notes,
                            photo_url = photo_url)  

        # Add new area to database
        db_session.add(new_person)
        db_session.commit()

        # Get person information
        person = Person.query.filter_by(email=email).first()

    except:
        flash("Person record was not added successfully. Please try again.",
              category='error')

    if person:
        description = f"add person {new_person.person_id}:{person.first_name} {person.last_name}"   
        
        # Add modification to database
        log_modification(description, new_person.date_added)

        return True, new_person
    else:
        return False, None
    

def add_person_affiliation(person_id=int, affiliation_type=''):
    person = Person.query.filter_by(person_id=person_id).first()
    affiliation = Affiliation.query.filter_by(affiliation_type=affiliation_type).first()
    description = f"add person-affiliation relation between \
          {person_id}:{person.first_name} {person.last_name} and \
            {affiliation.affiliation_id}:{affiliation.affiliation_type}"
    timestamp = now()

    try: 
        # Add person affiliations
        query = f'INSERT INTO person_affiliation \
                (fk_person_id, fk_affiliation_id) \
                VALUES \
                ({person_id}, {affiliation.affiliation_id});'
        execute(query)
        
        # Log modification 
        log_modification(description, timestamp)

    except:
        flash("Person affiliations could not be added.", category="error")
    
    
def add_person_support(person_id=int, entity_type='', entity_id=int, 
                       proficiency_id=int, notes='', notify=False):
    new_person_support = None
    description = f"add ({person_id}, {entity_id}) "
    timestamp = now()

    session = Session(engine)
    session.begin()
    try:
        if entity_type == "area":
            new_person_support = PersonArea(person_id, entity_id, proficiency_id, notes)
            description += f"to person_area"
        elif entity_type == "method":
            new_person_support = PersonMethod(person_id, entity_id, proficiency_id, notes)
            description += f"to person_method"
        elif entity_type == "tool":
            new_person_support = PersonTool(person_id, entity_id, proficiency_id, notes)
            description += f"to person_tool"

        session.add(new_person_support)
        session.commit()
    except:
        session.rollback()
        if notify:
            flash("Person support record(s) could not be added", category="error")
        return False
    
    # Add person support addition to modification log
    person_support = None
    if entity_type == "area":
        person_support = PersonArea.query.filter_by(fk_area_id=entity_id).first()
    elif entity_type == "method":
        person_support = PersonMethod.query.filter_by(fk_method_id=entity_id).first()
    elif entity_type == "tool":
        person_support = PersonTool.query.filter_by(fk_tool_id=entity_id).first()

    if person_support:
        # Add modification to database
        log_modification(description, timestamp)

    return True


def add_person_unit_to_db(person_id=int, person_name='', unit_name=''):
    print("person_id:", person_id, "person_name:", person_name, "unit_name:", unit_name)
    unit = Unit.query.filter_by(unit_name=unit_name).first()
    description = f"add person-unit relationship \
        between {person_id}:{person_name} and {unit.unit_id}:{unit.unit_name}"
    timestamp = now()

    try:
        query = f'INSERT INTO person_unit \
                (fk_person_id, fk_unit_id) \
                VALUES \
                ({person_id}, {unit.unit_id});'
        execute(query)

        # Add modification to database
        log_modification(description, timestamp)
        return True
    except:
        flash("Person-Unit relationship was not added successfully. Please try again.",
              category='error')
        return False


"""" Unit Functions """
def add_unit_to_db(unit_name, unit_type, email, web_address, phone, 
                   other_contact, preferred_contact, description, added_by):
    unit = None

    try:
        new_unit = Unit(unit_name = unit_name,
                        unit_type = unit_type,
                        email = email,
                        web_address = web_address,
                        phone = phone,
                        other_contact = other_contact,
                        preferred_contact = preferred_contact,
                        description = description,
                        added_by = added_by)

        # Add new Unit to database
        db_session.add(new_unit)
        db_session.commit()

        unit = Unit.query.filter_by(unit_name=unit_name).first()    
    except:
        flash("Unit record was not deleted successfully. Please try again.",
              category='error')

    if unit:
        mod_description = f"add unit {unit.unit_id}:{unit_name}" 

        # Add modification to database
        log_modification(mod_description, new_unit.date_added)

        return True, new_unit
    else:
         return False, None

    

def add_unit_subunit(subunit=Unit, parent_unit=Unit):
    description = f"add unit-subunit relationship \
        between {parent_unit.unit_id}:{parent_unit.unit_name} and \
        {subunit.unit_id}:{subunit.unit_name}"
    timestamp = now()

    # Add unit-subunit relation
    try:
        query = f'INSERT INTO unit_subunit \
                (fk_unit_id, subunit_id) \
                VALUES \
                ({parent_unit.unit_id}, {subunit.unit_id});'
        execute(query)

        # Log modificaiton
        log_modification(description, timestamp)
    except:
        flash("Unit-Parent Unit relationship was not added successfully. Please try again.",
              category='error')
        pass
    

def add_funding_unit_to_db(funding_id=int, funding_name='', unit_name=''):
    unit = Unit.query.filter_by(unit_name=unit_name).first()
    description = f"add unit-funding relationship \
        between {unit.unit_id}:{unit.unit_name} and \
        {funding_id}:{funding_name}"
    timestamp = now()

    try:
        query = f'INSERT INTO unit_funding \
                (fk_unit_id, fk_funding_id) \
                VALUES \
                ({unit.unit_id}, {funding_id});'
        execute(query)

        # Log modificaiton
        log_modification(description, timestamp)

        return True
    except:
        flash("Funding-Unit relationship was not added successfully. Please try again.",
              category='error')
        return False
    

def add_unit_resource(unit_id, unit_name, resource_id, resource_name, areas, 
                      notes):
    description = f"add unit-resource relationship \
        between {unit_id}:{unit_name} and \
        {resource_id}:{resource_name}"
    timestamp = now()

    try:
        # Add unit-resource relation
        query = f"INSERT INTO unit_resource \
                (fk_unit_id, fk_resource_id, notes) \
                VALUES \
                ({unit_id}, {resource_id},'{notes}');"
        execute(query)
        
        # Add resource-area relations in unit_support
        for area_name in areas:
            area = Area.query.filter_by(area_name=area_name).first()
            query = f"INSERT INTO unit_support \
                    (fk_unit_id, fk_area_id, fk_resource_id, date_added) \
                    VALUES \
                    ({unit_id}, {area.area_id}, {resource_id}, now());"
            execute(query)

        # log modification
        log_modification(description, timestamp)
    except:
        flash("Unit-resource relationship was not added successfully. Please try again.",
              category='error')


"""" Funding Functions """

def add_funding_to_db(funding_name, funding_type, duration, frequency, 
                      payment_type, payment_amount, career_level, web_address, 
                      notes, campus, added_by):
    # Create new funding object
    new_funding = Funding(funding_name = funding_name,
                          funding_type = funding_type,
                          duration = duration,
                          frequency = frequency,
                          payment_type = payment_type,
                          payment_amount = payment_amount,
                          career_level = career_level,
                          web_address = web_address,
                          notes = notes,
                          campus = campus,
                          added_by = added_by)

    # Add new Funding to database
    try:
        db_session.add(new_funding)
        db_session.commit()
    except:
        flash("The funding record could not be added", category="error")

    new_funding = Funding.query.filter_by(funding_name=funding_name).first()

    if new_funding:
        mod_description = f"add {new_funding.funding_id}:{new_funding.funding_name}"

        # Add modification to database
        log_modification(mod_description, new_funding.date_added)

        return True, new_funding
    else:
        return False, None


"""" Secondary Entity Functions """

def add_address_to_db(building_name=str, room_number=str, street_address=str, 
                address_2=str, city=str, state=str, zipcode=str, campus=str):
    new_address = Address(building_name=building_name, room_number=room_number,
                      street_address=street_address, address_2=address_2, 
                      city=city, state=state, zipcode=zipcode, campus=campus,
                      added_by=current_user.user_id)
        
    db_session.add(new_address)
    db_session.commit()

    success, address = get_address(building_name=building_name, room_number=room_number,
                          street_address=street_address, address_2=address_2, 
                          city=city, state=state, zipcode=zipcode, campus=campus)

    # Log modification
    description = f"add address {address.address_id}:{str(address)}"
    timestamp = address.date_added

    log_modification(description, timestamp)

    return success, address


def add_entity_address(entity_id=int, entity_name=str, entity_type=str, address_id=int):

    description = f"add {entity_type}-address relationship \
        between {entity_id}:{entity_name} and address {address_id}"
    timestamp = now()

    # Add new address, if any, and entity-address relation to db
    query = f"INSERT INTO {entity_type}_address\
            (fk_{entity_type}_id, fk_address_id) \
            VALUES \
            ({entity_id}, {address_id});"
    execute(query)

    # Log modification
    log_modification(description, timestamp)


def add_area_to_db(area_name):
    session = Session(engine)

    with session.begin():
        # Create new area object
        new_area = Area(area_name=area_name,
                        added_by=current_user.user_id)  

        # Add new area to database
        session.add(new_area)
        session.commit()
        
    # Get area information
    area = Area.query.filter_by(area_name=area_name).first()

    if area:
        description = f"add area {area.area_id}:{area_name}"
        # Add modification to database
        log_modification(description, area.date_added)

        return True, area
    else:
        return False, None

    
def add_method_to_db(method_name):
    session = Session(engine)

    with session.begin():
        # Create new method object
        new_method = Method(method_name=method_name,
                        added_by=current_user.user_id)  

        # Add new method to database
        session.add(new_method)
        session.commit()

    # Get method information
    method = Method.query.filter_by(method_name=method_name).first()

    if method:    
        description = f"add method {method.method_id}:{method_name}"
        # Add modification to database
        log_modification(description, method.date_added)

        return True, method
    else:
        return False, None


def add_tool_to_db(tool_name, tool_type, web_address):
    session = Session(engine)

    with session.begin():
        # Create new tool object
        new_tool = Tool(tool_name=tool_name,
                        tool_type=tool_type,
                        web_address=web_address,
                        added_by=current_user.user_id)  

        # Add new tool to database
        session.add(new_tool)
        session.commit()

    # Get tool information
    tool = Tool.query.filter_by(tool_name=tool_name).first()

    if tool:    
        description = f"add tool {tool.area_id}:{tool_name}"
        # Add modification to database
        log_modification(description, tool.date_added)

        return True, tool
    else:
        return False, None


def add_resource_to_db(resource_name, resource_type, web_address):
    session = Session(engine)

    with session.begin():
        # Create new resource object
        new_resource = Resource(resource_name=resource_name,
                                resource_type=resource_type,
                                web_addres=web_address,
                                added_by=current_user.user_id)  

        # Add new resource to database
        session.add(new_resource)
        session.commit()

    # Get resource information
    resource = Resource.query.filter_by(resource_name=resource_name).first()
    
    if resource:
        description = f"add resource {resource.area_id}:{resource_name}"
        # Add modification to database
        log_modification(description, resource.date_added)

        return True, resource
    else:
        return False, None


def add_resource_area(resource_id, resource_name, areas):
    # List for IDs and names of given areas 
    area_ids = []
    area_names = []

    # Add resource-area relations     
    for area_name in areas:
        area = Area.query.filter_by(area_name=area_name).first()
        if area:
            area_ids.append(area.area_id)
            area_names.append(area.area_name)

            # Set metadata for log
            description = f"update resource-area relation between \
                {resource_id}:{resource_name} and \
                {area.area_id}:{area.area_name}"
            timestamp = now() 

            try:
                query = f"INSERT INTO resource_area \
                        (fk_resource_id, fk_area_id) \
                        VALUES \
                        ({resource_id}, {area.area_id});"
                execute(query)
                
                # Log modification
                log_modification(description, timestamp)
            except:
                # Resource-area relationship already exists
                pass
