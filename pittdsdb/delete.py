from flask import Blueprint, request, jsonify, flash
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from flask_restful import Api, Resource
from functools import wraps
from datetime import datetime
from .database import db_session, engine
from .models import *
from .schemas import *
from .utilities import *


""" Functions Delete Records from the Data"""

def delete_person_from_db(person=Person):
    description = f"delete person {person.person_id}:{person.first_name} {person.last_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    db_session.execute(f'DELETE FROM person \
                       WHERE person_id = {person.person_id };')
    
    db_session.commit()
    
    # Log modification
    log_modification(description, timestamp)

    return


def delete_unit_from_db(unit=Unit):
    description = f"delete unit {unit.unit_id}:{unit.unit_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    db_session.execute(f'DELETE FROM unit \
                       WHERE unit_id = {unit.unit_id };')
    
    db_session.commit()
    
    # Log modification
    log_modification(description, timestamp)

    return


def delete_funding_from_db(funding=Funding):
    description = f"delete funding {funding.funding_id}:{funding.funding_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    db_session.execute(f'DELETE FROM funding \
                       WHERE funding_id = {funding.funding_id };')
    
    db_session.commit()
    
    # Log modification
    log_modification(description, timestamp)

    return


def delete_affiliations(person_id, person_name, 
                        affiliation_ids, affiliation_types):
    affiliations = []
    affiliation_ids_str = ", ".join(map(str, affiliation_ids))

    for i in range(len(affiliation_ids)):
        affiliations.append(f"{ affiliation_ids[i] }:{ affiliation_types[i] }")

    # Set log metadata
    description = f"delete person_affiliation relationship between \
        {person_id}:{person_name} and { affiliations }"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    db_session.execute(f'DELETE FROM person_affiliation \
                       WHERE fk_person_id = {person_id } \
                       AND fk_affiliation_id NOT IN ({affiliation_ids_str});')
    
    db_session.commit()
    
    # Log modification
    log_modification(description, timestamp)


def delete_address(address=Address):
    description = f"delete address {address.address_id}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    db_session.execute(f'DELETE FROM address \
                       WHERE address_id = {address.address_id };')
    
    db_session.commit()
    
    # Log modification
    log_modification(description, timestamp)


def delete_person_unit_from_db(person_id=int, unit_id=int):
    person = Person.query.filter_by(person_id=person_id).first()
    unit = Unit.query.filter_by(unit_id=unit_id).first()

    if not person or not unit:
        flash("Person ID or Unit ID is invalid", category="error")
    else:
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        description = f"delete person-unit relationship \
            between {person_id}:{person.first_name} {person.last_name} and \
                {unit_id}:{unit.unit_name}"

        # Delete person-subunit relation
        db_session.execute(f'DELETE FROM person_unit \
                        WHERE fk_person_id = { person_id }\
                        AND fk_unit_id = { unit_id };')
            
        db_session.commit()

        # Log modificaiton
        log_modification(description, timestamp)


def delete_unit_subunit(subunit=Unit, parent_unit=Unit):
    description = f"delete unit-subunit relationship \
        between {parent_unit.unit_id}:{parent_unit.unit_name} and \
        {subunit.unit_id}:{subunit.unit_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Delete unit-subunit relation
    db_session.execute(f'DELETE FROM unit_subunit \
                       WHERE fk_unit_id = { parent_unit.unit_id }\
                       AND subunit_id = { subunit.unit_id };')
        
    db_session.commit()

    # Log modificaiton
    log_modification(description, timestamp)


def delete_unit_funding(unit_id=int, unit_name='', 
                         funding_id=int, funding_name=''):
    description = f"delete unit-funding relationship between \
        {unit_id}:{unit_name} and {funding_id}:{funding_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    db_session.execute(f"DELETE FROM unit_funding \
                       WHERE fk_unit_id = {unit_id} \
                       AND fk_funding_id = {funding_id};")
    
    # Commit all changes to the database
    db_session.commit()
    
    # Log modificaiton
    log_modification(description, timestamp)


def delete_unit_resource(unit_id=int, unit_name='', 
                         resource_id=int, resource_name=''):
    description = f"delete unit-resource relationship between \
        {unit_id}:{unit_name} and {resource_id}:{resource_name}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    db_session.execute(f"DELETE FROM unit_resource \
                       WHERE fk_unit_id = {unit_id} \
                       AND fk_resource_id = {resource_id};")
    
    # Log modificaiton
    log_modification(description, timestamp)
    
    # Check if the resource is still supported by any other unit(s)
    resource_supported = db_session.execute(
        f"SELECT * FROM vw_unit_support \
        WHERE resource_id = { resource_id };")
    
    # Delete resource if it is no longer supported
    if not resource_supported:
        description = f"delete {resource_id}:{resource_name} (no longer supported)"
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        db_session.execute(f"DELETE FROM resource \
                           WHERE resource_id = { resource_id };")
        
        # Log modification
        log_modification(description, timestamp)
    
    # Commit all changes to the database
    db_session.commit()


def delete_entity_address(entity_id=int, entity_name=str, 
                          entity_type=str, address_id=int):
    description = f"delete {entity_type}-address relationship between \
        {entity_type} {entity_id}:{entity_name} and address {address_id}"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    db_session.execute(f"DELETE FROM {entity_type}_address \
                       WHERE fk_{entity_type}_id = {entity_id} \
                       AND fk_address_id = {address_id};")
    
    # Log modificaiton
    log_modification(description, timestamp)

def delete_entity_area(entity_type, entity_id, entity_name, area_names):
    # Get list of IDs for areas in given list
    area_ids = []
    for name in area_names:
        area = Area.query.filter_by(area_name=name).first()
        area_ids.append(area.area_id)

    # Convert list to string for SQL query
    area_ids_str = ", ".join(map(str, area_ids))

    # Get IDs for areas that may need to be deleted
    results = db_session.execute(f"SELECT fk_area_id FROM { entity_type }_area \
                                 WHERE fk_{ entity_type }_id = { entity_id } \
                                 AND fk_area_id NOT IN ({ area_ids_str});").fetchall()
    
    # Delete current entities relationships1
    
    
    # Queue areas to check if a relation with given entity still exists
    areas_to_check = []
    for res in results:
        area = Area.query.filter_by(area_id=res[0]).first()
        areas_to_check.append(area)
    
    # Check if area(s) is/are associated with entity in support table 
    # and queue for deletion if not
    areas_to_delete = []
    areas_to_delete_ids = []
    for area in areas_to_check:
        if entity_type == "resource":
            still_exists = check_relation("vw_unit_support", entity_type, entity_id,
                                        "area", area.area_id)
        else:
            still_exists = check_relation("vw_person_support", entity_type, entity_id,
                                        "area", area.area_id)
        if not still_exists:
            areas_to_delete.append(f"{ area.area_id }:{ area.area_name }")
            areas_to_delete_ids.append(area.area_id)

    # Set log metadata
    areas_to_delete_str = ", ".join(areas_to_delete)
    
    description = f"delete { entity_type }_area relationship between \
        {entity_id}:{entity_name} and { areas_to_delete_str }"
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Delete from area 
    for area_id in areas_to_delete_ids:
        if entity_type in ["method", "tool"]:
            db_session.execute(f"DELETE FROM person_support \
                                WHERE { entity_id } = { entity_id } \
                                AND fk_area_id IN ({ areas_to_delete_str});")
        if entity_type in ["resource"]:
            db_session.execute(f"DELETE FROM person_support \
                                WHERE { entity_id } = { entity_id } \
                                AND fk_area_id IN ({ areas_to_delete_str});")
    
    # probably need to do this differently for tools, need to know the method as well
    
        # Delete defunct entity-area relations 
        db_session.execute(f"DELETE FROM { entity_type }_area \
                        WHERE fk_{ entity_type }_id = { entity_id } \
                        AND fk_area_id NOT IN ({ area_ids_str});")
    
    # Log modification
    log_modification(description, timestamp)


    
    

    

