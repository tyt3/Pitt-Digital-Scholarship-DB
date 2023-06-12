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
    timestamp = now()
    
    try:
        query = f'DELETE FROM person WHERE person_id = {person.person_id};'
        execute(query)
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("Person record was not deleted successfully. Please try again.",
              category='error')


def delete_unit_from_db(unit=Unit):
    description = f"delete unit {unit.unit_id}:{unit.unit_name}"
    timestamp = now()
    try:
        query = f'DELETE FROM unit WHERE unit_id = {unit.unit_id};'
        execute(query)
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("Unit record was not deleted successfully. Please try again.",
              category='error')


def delete_funding_from_db(funding=Funding):
    description = f"delete funding {funding.funding_id}:{funding.funding_name}"
    timestamp = now()
    try:
        query = f'DELETE FROM funding WHERE funding_id = {funding.funding_id};'
        execute(query)
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("Person record was not deleted successfully. Please try again.",
              category='error')


def delete_affiliations(person_id, person_name, 
                        affiliation_ids, affiliation_types):
    affiliations = []
    try:
        affiliation_ids_str = ", ".join(map(str, affiliation_ids))

        for i in range(len(affiliation_ids)):
            affiliations.append(f"{affiliation_ids[i]}:{affiliation_types[i]}")

        # Set log metadata
        description = f"delete person_affiliation relationship between \
            {person_id}:{person_name} and {affiliations}"
        timestamp = now()
        query = f'DELETE FROM person_affiliation \
                WHERE fk_person_id = {person_id} \
                AND fk_affiliation_id NOT IN ({affiliation_ids_str});'
        execute(query)
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("Person-Affiliation relationship was not deleted successfully. Please try again.",
                category="error")


def delete_address(address=Address):
    description = f"delete address {address.address_id}"
    timestamp = now()
    
    try:
        # Delete address
        query = f'DELETE FROM address WHERE address_id = {address.address_id};'
        execute(query)
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("Address was not deleted successfully. Please try again.",
                category="error")


def delete_person_unit_from_db(person_id=int, unit_id=int):
    person = Person.query.filter_by(person_id=person_id).first()
    unit = Unit.query.filter_by(unit_id=unit_id).first()

    if not person or not unit:
        flash("Person ID or Unit ID is invalid", category="error")
    else:
        timestamp = now()
        description = f"delete person-unit relationship \
            between {person_id}:{person.first_name} {person.last_name} and \
                {unit_id}:{unit.unit_name}"

        try:
            # Delete person-subunit relation
            query = f'DELETE FROM person_unit \
                    WHERE fk_person_id = {person_id}\
                    AND fk_unit_id = {unit_id};'
            execute(query)
                
            # Log modificaiton
            log_modification(description, timestamp)
        except:
            flash("Person-Unit relationship was not deleted successfully. Please try again.",
                category="error")


def delete_unit_subunit(subunit=Unit, parent_unit=Unit):
    description = f"delete unit-subunit relationship \
        between {parent_unit.unit_id}:{parent_unit.unit_name} and \
        {subunit.unit_id}:{subunit.unit_name}"
    timestamp = now()

    try:
        # Delete unit-subunit relation
        query = f'DELETE FROM unit_subunit \
                WHERE fk_unit_id = {parent_unit.unit_id}\
                AND subunit_id = {subunit.unit_id};'
        execute(query)

        # Log modificaiton
        log_modification(description, timestamp)
    except:
        flash("Unit-Subunit relationship was not deleted successfully. Please try again.",
                category="error")


def delete_unit_funding(unit_id=int, unit_name='', 
                         funding_id=int, funding_name=''):
    description = f"delete unit-funding relationship between \
        {unit_id}:{unit_name} and {funding_id}:{funding_name}"
    timestamp = now()
    
    try:
        query= f"DELETE FROM unit_funding \
                WHERE fk_unit_id = {unit_id} \
                AND fk_funding_id = {funding_id};"
        execute(query)
        
        # Log modificaiton
        log_modification(description, timestamp)
    except:
        flash("Unit-Funding relationship was not deleted successfully. Please try again.",
                category="error")
        

def delete_unit_resource(unit_id=int, unit_name='', 
                         resource_id=int, resource_name=''):
    description = f"delete unit-resource relationship between \
        {unit_id}:{unit_name} and {resource_id}:{resource_name}"
    timestamp = now()
    
    try:
        query = f"DELETE FROM unit_resource \
                WHERE fk_unit_id = {unit_id} \
                AND fk_resource_id = {resource_id};"
        execute(query)
        
        # Log modificaiton
        log_modification(description, timestamp)
    except:
        flash("Unit-Resource relationship was not deleted successfully. Please try again.",
                category="error")
    
    # Check if the resource is still supported by any other unit(s)
    query = f"SELECT * FROM vw_unit_support WHERE resource_id = {resource_id};"
    resource_supported = execute(query, "first")
    
    # Delete resource if it is no longer supported
    if not resource_supported:
        description = f"delete {resource_id}:{resource_name} (no longer supported)"
        timestamp = now()

        try:
            query = f"DELETE FROM resource WHERE resource_id = {resource_id};"
            execute(query)
            
            # Log modification
            log_modification(description, timestamp)
        except:
            print("Query failed:", query)


def delete_entity_address(entity_id=int, entity_name=str, 
                          entity_type=str, address_id=int):
    description = f"delete {entity_type}-address relationship between \
        {entity_type} {entity_id}:{entity_name} and address {address_id}"
    timestamp = now()
    
    try:
        # Delete entity address
        query = f"DELETE FROM {entity_type}_address \
                WHERE fk_{entity_type}_id = {entity_id} \
                AND fk_address_id = {address_id};"
        execute(query)
    
        # Log modificaiton
        log_modification(description, timestamp)
    except:
        flash(f"{entity_type}-Address relationship was not deleted successfully. Please try again.",
                category="error")


def delete_entity_area(owner_id=int, entity_type=str, entity_id=int, 
                       entity_name=str, area_names=str):
    # Get list of IDs for areas in given list
    area_ids = []
    for name in area_names:
        area = Area.query.filter_by(area_name=name).first()
        area_ids.append(area.area_id)

    # Convert list to string for SQL query
    area_ids_str = ", ".join(map(str, area_ids))

    results = []
    try:
        # Get IDs for areas not in given list
        query = f"SELECT fk_area_id FROM {entity_type}_area \
                WHERE fk_{entity_type}_id = {entity_id} \
                AND fk_area_id NOT IN ({area_ids_str});"
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)
    
    for area_id in results:
        # Get area record
        area = Area.query.filter_by(area_id=area_id[0]).first()
        
        if entity_type == "resource": 
            owner = Unit.query.filter_by(unit_id=owner_id).first()
            owner_type = "unit"
            owner_name = owner.unit_name
            table = "unit_support"
        else:
            owner = Person.query.filter_by(person_id=owner_id).first()
            owner_type = "person" 
            owner_name = owner.first_name + " " + owner.last_name
            table = "person_support"
        
        # Delete from person's support record
        # Set metadata from deletion
        description = f"delete {entity_type}-area relationship between \
            {entity_id}:{entity_name} and {area.area_id}:{area.area_name} \
            from {owner_id}:{owner_name}'s record"
        timestamp = now()

        # Delete defunct entity-area relations 
        try:
            query = f"DELETE FROM {table} \
                    WHERE fk_{owner_type}_id = {owner_id} \
                    AND fk_{entity_type}_id = {entity_id} \
                    AND fk_area_id = {area.area_id};"
            execute(query)

            # Log modification
            log_modification(description, timestamp)
        except:
            print("Query failed:", query)

        # Check if there are any remaining relationships with area in table
        still_exists = check_relation(f"{owner_type}_support", entity_type, 
                                        entity_id, "area", area.area_id)
        
        if not still_exists:
            # Set metadata from deletion
            description = f"delete {entity_type}_area relationship between \
                {entity_id}:{entity_name} and {area.area_id}:{area.area_name}"
            timestamp = now()

            try:
                # Delete defunct entity-area relations 
                query = f"DELETE FROM {entity_type}_area \
                        WHERE fk_{entity_type}_id = {entity_id} \
                        AND fk_area_id = {area.area_id};"
                execute(query)

                # Log modification
                log_modification(description, timestamp)
            except:
                print("Query failed:", query)
            
            # Check people and unit support and delete area if in neither
            unit_supported = check_entity(f"vw_unit_support", "area", area.area_id)
            person_supported = check_entity(f"vw_person_support", "area", area.area_id)
            
            if not unit_supported and not person_supported:
                # Set metadata from deletion
                description = f"delete {area.area_id}:{area.area_name}"
                timestamp = now()

                try:
                    # Delete area
                    query = f"DELETE FROM area WHERE area_id = {area.area_id};"
                    execute(query)

                    # Log modification
                    log_modification(description, timestamp)
                except:
                    print("Query failed:", query)
        else:
            print("still exists")


def delete_method_tool(person_id, tool_id, tool_name, method_names):
    # Get person record
    person = Person.query.filter_by(person_id=person_id).first()

    # Get list of IDs for areas in given list
    method_ids = []
    for name in method_names:
        method = Method.query.filter_by(method_name=name).first()
        method_ids.append(method.method_id)

    # Convert list to string for SQL query
    method_ids_str = ", ".join(map(str, method_ids))

    # Get IDs for areas not in given list
    results = []
    try:
        query = f"SELECT fk_method_id FROM method_tool \
                WHERE fk_tool_id = {tool_id} \
                AND fk_method_id NOT IN ({method_ids_str});"
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)
    
    for res in results:
        method_id = res[0]
        # Get method record
        method = Method.query.filter_by(method_id=method_id).first()

        # Delete from person's support record
        # Set metadata from deletion
        description = f"delete method-tool relationship between \
            {method_id}:{method.method_name} and {tool_id}:{tool_name} from\
                {person_id}:{person.first_name} {person.last_name}'s record"
        timestamp = now()

        # Delete defunct entity-area relations 
        try:
            query = f"DELETE FROM person_support \
                    WHERE fk_person_id = {person_id} \
                    AND fk_method_id = {method_id} \
                    AND fk_tool_id = {tool_id};"
            execute(query)

            # Log modification
            log_modification(description, timestamp)
        except:
            print("Query failed:", query)

        # Check if there are any remaining relationships with area in table
        still_exists = check_relation(f"person_support", "tool", 
                                        tool_id, "method", method_id)

        if not still_exists:
            # Set metadata from deletion
            description = f"delete method-tool relationship between \
                {method_id}:{method.method_name} and {tool_id}:{tool_name}"
            timestamp = now()

            try:
                # Delete defunct entity-area relations 
                query = f"DELETE FROM method_tool \
                        WHERE fk_method_id = {method_id} \
                        AND fk_tool_id = {tool_id};"
                execute(query)

                # Log modification
                log_modification(description, timestamp)
            except:
                print("Query failed:", query)
            
            # Check people support and delete area if not
            supported = check_entity(f"vw_person_support", "method", method_id)
            
            if not supported:
                # Set metadata from deletion
                description = f"delete {method_id}:{method.method_name}"
                timestamp = now()

                try:
                    # Delete area
                    query = f"DELETE FROM method WHERE method_id = {method_id};"
                    execute(query)

                    # Log modification
                    log_modification(description, timestamp)
                except:
                    print("Query failed:", query)
                