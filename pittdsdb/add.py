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


def sp_ManagePersonArea(method=str, user_id=int, person_id=int, area_name=str,
                        new_name='', area_proficiency=str, area_notes=''):
    input_list = [method, user_id, person_id, area_name, new_name, 
                  area_proficiency, area_notes, False, None]
    results = None

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonArea", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results


def sp_ManagePersonMethod(method=str, user_id=int, person_id=int, area_name=str,
                          method_name=str, new_name=str, proficiency=str, 
                          notes=str):
    input_list = [method, user_id, person_id, area_name, method_name, new_name, 
                  proficiency, notes, False, None]
    results = None

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonMethod", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results


def sp_ManagePersonTool(method=str, user_id=int, person_id=int, area_name=str,
                        method_name=str, tool_name=str, tool_type=str,
                        web_address=str, new_name=str,  proficiency=str, 
                        notes=str):
    input_list = [method, user_id, person_id, area_name, method_name, tool_name,
                  tool_type, web_address, new_name, proficiency, notes, False, 
                  None]
    results = None

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonTool", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results


def add_modification(timestamp, description):
    modification = Modification(modification=description,
                                modified_by=current_user.user_id,
                                modification_date=timestamp)
    
    # Add modification log to database
    db_session.add(modification)
    db_session.commit()


def add_person_to_db(first_name, last_name, title, pronouns, email, web_address,
                     phone, scheduler_address, other_contact, preferred_contact,
                     support_type, bio, added_by, notes, photo_url):

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

    if person:
        # Add modification to database
        add_modification(new_person.date_added, f"add {repr(person)}")
        
        print("person added")
        return True, new_person
    else:
        return False, None
    


def add_person_affiliation(person_id=int, affiliation_type=str):
    affiliation = Affiliation.query.filter_by(affiliation_type=affiliation_type).first()
 
    session = Session(engine)
    session.begin()
    try:
        session.execute(f'INSERT INTO person_affiliation \
                        (fk_person_id, fk_affiliation_id) \
                        VALUES \
                        ({ person_id }, { affiliation.affiliation_id })')
        session.commit()

        return True
    except:
        session.rollback()
        flash("Person affiliation(s) could not be added", category="error")
        return False
    
    
def add_person_support(person_id=int, entity_type=str, entity_id=int, 
                       proficiency_id=int, notes=str, notify=False):
    new_person_support = None
    description = f"add ({ person_id }, { entity_id }) "

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
            print("Person support record(s) could not be added")
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
        add_modification(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), description)

    return True


def add_person_support_combos(person_id=int, area_id=int, method_id=0, tool_id=0):
    session = Session(engine)

    session.begin()
    # Add method area relationship
    try:
        session.execute(f"INSERT INTO method_area \
                        (fk_method_id, fk_area_id) \
                        VALUES \
                        ({ method_id }, { area_id });")
        session.commit()
    except:
        session.rollback()
        print("Method/area relationship could not be added")
        return False

    # Build query
    if method_id > 0 and tool_id > 0:
        # Add tool area relationship
        session.begin()
        try:
            session.execute(f"INSERT INTO tool_area \
                            (fk_tool_id, fk_area_id) \
                            VALUES \
                            ({ tool_id }, { area_id });")
            session.commit()
        except:
            print("Tool/area relationship could not be added.")

        # Add method tool relationship
        with session.begin():
            session.execute(f"INSERT INTO method_area \
                            (fk_method_id, fk_area_id) \
                            VALUES \
                            ({ method_id }, { tool_id });")
            session.commit()
            
        # Query for existing person support relations
        person_support = db_session.execute(f'SELECT * FROM person_support \
                                            WHERE fk_person_id = { person_id } \
                                            AND fk_area_id = { area_id } \
                                            AND fk_method_id = { method_id } \
                                            AND fk_tool_id IS NULL;')
        
        # Check if person-area-method relationship already in person_support
        if person_support.rowcount > 0:
            # Update existing record
            session.begin()
            try:
                session.execute(f'UPDATE person_support \
                                SET \
                                fk_tool_id = { tool_id } \
                                WHERE fk_person_id = { person_id } \
                                AND fk_area_id = { area_id } \
                                AND fk_method_id = { method_id };')
                session.commit()
            except:
                session.rollback()
                print("Person support record could not be added")
                return False
        else:
            # Add new record
            session.begin()
            try:
                session.execute(f'INSERT INTO person_support \
                                (fk_person_id, fk_area_id, fk_method_id, fk_tool) \
                                VALUES \
                                ({ person_id }, { area_id }, \
                                { method_id }, { tool_id });')
                session.commit()
            except:
                session.rollback()
                print("Person support record could not be added")
                return False
    elif method_id > 0:
        # Add person support relations
        person_support = db_session.execute(f'SELECT * FROM person_support \
                                            WHERE fk_person_id = { person_id } \
                                            AND fk_area_id = { area_id } \
                                            AND fk_method_id IS NULL;')
        
        # Check if person-area-method relationship already in person_support
        if person_support.rowcount > 0:
            # Update existing record
            session.begin()
            try:
                session.execute(f'UPDATE person_support \
                                SET \
                                fk_method_id = { method_id } \
                                WHERE fk_person_id = { person_id } \
                                AND fk_area_id = { area_id };')
                session.commit()
            except:
                session.rollback()
                print("Person support record could not be added")
                return False
        else:
            # Add new record
            session.begin()
            try:
                session.execute(f'INSERT INTO person_support \
                                (fk_person_id, fk_area_id, fk_method_id) \
                                VALUES \
                                ({ person_id }, { area_id }, { method_id });')
                session.commit()
            except:
                session.rollback()
                print("Person support record could not be added")
                return False

    
def add_person_unit_to_db(person_id=int, unit_name=str):
    unit = Unit.query.filter_by(unit_name=unit_name).first()

    try:
        db_session.execute(f'INSERT INTO person_unit \
                        (fk_person_id, fk_unit_id) \
                        VALUES \
                        ({ person_id }, { unit.unit_id })')
        db_session.commit()
        return True
    except:
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
    

def add_unit_to_db(unit_name, unit_type, email, web_address, phone, 
                   other_contact, preferred_contact, description, added_by):
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

     if unit:
        # Add modification to database
        add_modification(new_unit.date_added, 
                         f"add {repr(new_unit)}")

        return True, new_unit
     else:
         return False, None


def add_subunit_to_db(subunit_name, subunit_type, email, web_address, phone, 
                      other_contact, preferred_contact, description, 
                      parent_unit_name, added_by):
    # Get parent unit name
    parent_unit = Unit.query.filter_by(unit_name=parent_unit_name).first()
    parent_unit_id = parent_unit.get_id()

    new_subunit = Subunit(subunit_name = subunit_name,
                              subunit_type = subunit_type,
                              email = email,
                              web_address = web_address,
                              phone = phone,
                              other_contact = other_contact,
                              preferred_contact = preferred_contact,
                              description = description,
                              fk_unit_id=parent_unit_id,
                              added_by = added_by)

    # Add new department to database
    db_session.add(new_subunit)
    db_session.commit()

    subunit = Subunit.query.filter_by(subunit_name=subunit_name).first()

    if subunit:
        # Add modification to database
        add_modification(new_subunit.date_added,
                         f"add {repr(new_subunit)}")

        return True, new_subunit
    else:
        return False, None


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
        # Add modification to database
        add_modification(new_area.date_added, f"add {repr(new_area)}")

        return True, new_area
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
        # Add modification to database
        add_modification(new_method.date_added, f"add {repr(new_method)}")
        return True, new_method
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
        # Add modification to database
        add_modification(new_tool.date_added, f"add {repr(new_tool)}")

        return True, new_tool
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
        # Add modification to database
        add_modification(new_resource.date_added, f"add {repr(new_resource)}")

        return True, new_resource
    else:
        return False, None

