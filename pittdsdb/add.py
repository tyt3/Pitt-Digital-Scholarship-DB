from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
from .database import db_session
from .models import *
from .schemas import *


def add_modification(entity, entity_type, description):
    # Get details
    user_id = current_user.user_id
    timestamp = entity.date_added

    modification = Modification(entity_type=entity_type,
                                entity_id=entity.get_id(),
                                modification=description,
                                modified_by=user_id,
                                modification_date=timestamp)
    
    # Add modification log to database
    db_session.add(modification)
    db_session.commit()


def add_area_to_db(name):
    area_name = name.title()
    area = Area.query.filter_by(area_name=area_name).first()
    
    if area:
        return False
    else:
        # Create new area object
        new_area = Area(area_name=area_name)  

        # Add new area to database
        db_session.add(new_area)
        db_session.commit()

        # Add modification to database
        add_modification(new_area, "area", f"add {repr(new_area)}")

    return True, new_area

    
def add_method_to_db(name):
    method_name = name.title()
    method = Method.query.filter_by(method_name=method_name).first()
    
    if method:
        return False
    else:
        # Create new area object
        new_method = Method(method_name=method_name)  

        # Add new area to database
        db_session.add(new_method)
        db_session.commit()

        # Add modification to database
        add_modification(new_method, "method", f"add {repr(new_method)}")

    return True


def add_person_to_db(first_name, last_name, title, pronouns, email,
                 web_address, phone, scheduler_address, preferred_contact, 
                 support_type, bio, added_by, notes):
    person = Person.query.filter_by(email=email).first()
    
    if person:
        return False
    else:
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
                            support_type = support_type,
                            bio = bio,
                            added_by = added_by,
                            notes = notes)  

        # Add new area to database
        db_session.add(new_person)
        db_session.commit()

        # Add modification to database
        add_modification(new_person, "person", f"add {repr(new_person)}")

    return True, new_person


def add_person_affiliation(person_id=int, affiliation_type=str):
    affiliation = Affiliation.query.filter_by(affiliation_type=affiliation_type).first()
    print(affiliation.affiliation_type)

    try:
        db_session.execute(f'INSERT INTO person_affiliation \
                        (fk_person_id, fk_affiliation_id) \
                        VALUES \
                        ({ person_id }, { affiliation.affiliation_id })')
        db_session.commit()

        return True
    except:
        return False
    

def add_person_unit_to_db(person_id=int, unit_name=str):
    unit = Unit.query.filter_by(unit_name=unit_name).first()
    print("unit", unit)

    try:
        db_session.execute(f'INSERT INTO person_unit \
                        (fk_person_id, fk_unit_id) \
                        VALUES \
                        ({ person_id }, { unit.unit_id })')
        db_session.commit()
        print("added unit")
        return True
    except:
        print("unit wasn't added")
        return False


def add_person_subunit_to_db(person_id=int, subunit_name=str):
    subunit = Subunit.query.filter_by(subunit_name=subunit_name).first()

    try:
        db_session.execute(f'INSERT INTO person_subunit \
                        (fk_person_id, fk_subunit_id) \
                        VALUES \
                        ({ person_id }, { subunit.subunit_id })')
        db_session.commit()
        return True
    except:
        return False


def add_resource_to_db(name, resource_type):
    resource_name = name.title()
    resource = Resource.query.filter_by(resource_name=resource_name).first()
    
    if resource:
        return False
    else:
        # Create new area object
        new_resource = Resource(resource_name=resource_name,
                                resource_type=resource_type)  

        # Add new area to database
        db_session.add(new_resource)
        db_session.commit()

        # Add modification to database
        add_modification(new_resource, "area", f"add {repr(new_resource)}")

    return True


def add_subunit_to_db(name, subunit_type, email, web_address, phone, 
                 preferred_contact, description, parent_unit_name):
    subunit_name = name.title()
    subunit = Subunit.query.filter_by(subunit_name=subunit_name).first()
    
    if subunit:
        return False
    else:
        # Get parent unit name
        parent_unit = Unit.query.filter_by(unit_name=parent_unit_name).first()
        parent_unit_id = parent_unit.get_id()

        # Create new department object
        new_subunit = Subunit(subunit_name = subunit_name,
                              subunit_type = subunit_type,
                              email = email,
                              web_address = web_address,
                              phone = phone,
                              preferred_contact = preferred_contact,
                              description = description)  

        # Add new department to database
        db_session.add(new_subunit)
        db_session.commit()

        # Add modification to database
        add_modification(new_subunit, "department", 
                         f"add {repr(new_subunit)}")

    return True


def add_tool_to_db(name, web_address, github):
    tool_name = name.title()
    tool = Tool.query.filter_by(tool_name=tool_name).first()
    
    if tool:
        return False
    else:
        # Create new area object
        new_tool = Tool(tool_name=tool_name)  

        # Add new area to database
        db_session.add(new_tool)
        db_session.commit()

        # Add modification to database
        add_modification(new_tool, "tool", f"add {repr(new_tool)}")

    return True


def add_unit_to_db(name, unit_type, email, web_address, phone, preferred_contact, description):
    unit_name = name.title()
    unit = Unit.query.filter_by(unit_name=unit_name).first()
    
    if unit:
        return False
    else:
        # Create new department object
        new_unit = Unit(unit_name = unit_name,
                        unit_type = unit_type,
                        email = email,
                        web_address = web_address,
                        phone = phone,
                        preferred_contact = preferred_contact,
                        description = description)  

        # Add new department to database
        db_session.add(new_unit)
        db_session.commit()

        # Add modification to database
        add_modification(new_unit, "unit", 
                         f"add {repr(new_unit)}")

    return True

