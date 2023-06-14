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
from .add import *
from .delete import *
from .utilities import *


def update_user(first_name=str, last_name=str, user_name=str, email=str,
                password=str, permission_level=int):
    current_user.first_name=first_name
    current_user.last_name=last_name,
    current_user.user_name=user_name,
    current_user.email=email,
    current_user.user_password=password,
    current_user.fk_permission_id=permission_level

    try:
        db_session.commit()

        # Alert user that account was created succesfully
        flash("Account details updated!", category="success")
        
        # Log modification
        description = f"update user {current_user.user_id}:{current_user.first_name} \
            {current_user.last_name}"
        log_modification(description, now(), current_user.user_id)
    except:
        # Alert user that account was created succesfully
        flash("Account could not be updated.", category="error")


def update_person(person=Person, first_name='', last_name='', pronouns='', 
                  title='', email='', phone='', scheduler_address='', 
                  other_contact='', preferred_contact='', web_address='', 
                  support_type='', bio='', notes='', photo_url=''):
    description = f"update person {person.person_id}:{person.first_name} {person.last_name}"
    timestamp = now()  

    # Update person record
    person.first_name = first_name
    person.last_name = last_name
    person.pronouns = pronouns
    person.title = title
    person.email = email
    person.phone = phone
    person.scheduler_address = scheduler_address
    person.other_contact = other_contact
    person.preferred_contact = preferred_contact
    person.web_address = web_address
    person.support_type = support_type
    person.bio = bio
    person.notes = notes
    person.photo_url = photo_url

    # Commit changes
    try:
        db_session.commit()
        
        # Log modification
        log_modification(description, timestamp)
    except:
        flash("The unit record could not be updated.", category="error")


def update_unit(unit=Unit, unit_name='', unit_type='', email='', phone='', 
                other_contact='', preferred_contact='', web_address='', \
                description=''):
    # Set metadata for log
    mod_description = f"update unit {unit.unit_id}:{unit.unit_name}"
    timestamp = now()   

    # Update unit record
    unit.unit_name = unit_name
    unit.unit_type = unit_type
    unit.email = email
    unit.web_address = web_address
    unit.phone = phone
    unit.other_contact = other_contact
    unit.preferred_contact = preferred_contact
    unit.description = description
    unit.last_modified = timestamp  

    # Commit changes
    try:
        db_session.commit()

        # Log modification
        log_modification(mod_description, timestamp)
    except:
        flash("The person record could not be updated.", category="error")


def update_funding_in_db(funding=Funding, funding_name='', funding_type='',
                         duration='', frequency='', payment_type='', 
                         payment_amount='', career_level='', web_address='', 
                         notes='', campus=''):
    description = f"update funding {funding.funding_id}:{funding.funding_name}"
    timestamp = now()  

    # Update funding record
    funding.funding_name = funding_name
    funding.funding_type = funding_type
    funding.duration = duration
    funding.frequency = frequency
    funding.payment_type = payment_type
    funding.payment_amount = payment_amount
    funding.career_level = career_level
    funding.web_address = web_address
    funding.notes = notes
    funding.campus = campus
    funding.last_modified = timestamp

    # Commit changes
    try:
        db_session.commit()

        # Log modification
        log_modification(description, timestamp)
    except:
        flash("The funding record could not be updated.", category="error")
   

def update_address(entity_type=str, entity_id=str, entity_public_id=int, 
                   entity_name=str, address=Address, building_name=str, 
                   room_number=str, street_address=str, address_2=str, 
                   city=str, state=str, zipcode=str, campus=str):
    # Check if other entities share ddress
    query = f"SELECT * FROM vw_addresses \
            WHERE address_id = '{address.address_id}'\
            AND public_id <> '{entity_public_id}';"
    results = execute(query, 'fetchall')
    
    if results:
        # Other entities are associated with address, so a new one should be added
        delete_entity_address(entity_id, entity_name, 
                              entity_type, address.address_id)
        success, address = add_address_to_db(building_name=building_name, 
                                             room_number=room_number,
                                             street_address=street_address,
                                             address_2=address_2, 
                                             city=city, state=state, 
                                             zipcode=zipcode, campus=campus)
        add_entity_address(entity_id, entity_name,
                           entity_type, address.address_id)
    else:
        # Check if updated address is already in the database
        exists, existing_address = get_address(building_name, room_number, 
                                               street_address, address_2, city, 
                                               state, zipcode, campus)
        if exists:
            # Delete current address
            delete_address(address)

            # Add entity-address relationship with existing address
            add_entity_address(entity_id, entity_name, entity_type,
                               existing_address.address_id)
        else:
            # Set metadata for log
            description = f"update address {address.address_id}"
            timestamp = now()   

            address.building_name = building_name
            address.room_number = room_number
            address.street_address = street_address
            address.address_2 = address_2
            address.city = city
            address.state = state
            address.zipcode = zipcode
            address.campus = campus 
            address.last_modified = timestamp

            try:
                db_session.commit()
                
                # Log modification
                log_modification(description, timestamp)
            except:
                flash("The address record could not be updated.", category="error")


def update_affiliations(person_id, person_name, affiliations):
    affiliation_ids = []
    affiliation_types = []

    for a in affiliations:
        affiliation = Affiliation.query.filter_by(affiliation_type=a).first()
        exists = check_relation("person_affiliation", "person", person_id, 
                                "affiliation", affiliation.affiliation_id)
        if not exists:
            add_person_affiliation(person_id, a)

        affiliation_ids.append(affiliation.affiliation_id)
        affiliation_types.append(affiliation.affiliation_type)

    delete_affiliations(person_id, person_name, 
                        affiliation_ids, affiliation_types)


def update_unit_resource(unit_id=int, unit_name=str, resource=Resource, 
                         areas=[], new_resource_name='', resource_type='',
                         web_address='', notes=''):
    # Set metadata for log
    description = f"update {resource.resource_id}:{resource.resource_name}"
    timestamp = now()        

    # Update resource record
    if new_resource_name:
        resource.resource_name = new_resource_name
    resource.resource_type = resource_type
    resource.web_address = web_address
    resource.last_modified = timestamp

    try:
        db_session.commit()

        # Log modification
        log_modification(description, timestamp)
    except:
        flash("The unit resource record could not be updated.", category="error")

    # Set metadata for log
    description = f"update unit-resource relation between {unit_id}:{unit_name} \
        and {resource.resource_id}:{resource.resource_name}"
    timestamp = now()

    # Update notes
    query = f"UPDATE unit_resource \
            SET notes = '{notes}' \
            WHERE fk_unit_id = {unit_id} \
            AND fk_resource_id = {resource.resource_id};"
    execute(query)
    
    try:
        db_session.commit()

        # Log modification
        log_modification(description, timestamp)
    except:
        flash("The unit resource record could not be updated.", category="error")

    # add resource-area relation for areas in given list
    add_resource_area(resource.resource_id, resource.resource_name, areas)

    # delete resource-area relation for areas not in given list, if any
    delete_entity_area(unit_id, "resource", resource.resource_id, 
                       resource.resource_name, areas)
