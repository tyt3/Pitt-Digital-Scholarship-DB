from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
import pandas as pd
import re
from markdown import markdown
from .database import db_session, engine
from .models import *
from .schemas import *
from .utilities import *


""" Person Get Functions """

def get_person_relations(person_id=int, public_id=str, 
                         column=str, entity_type=str, entity_id=0) -> list:
    results = results_list = []

    if entity_type == 'unit':
        results = get_person_units('person', public_id) 

        for result in results:
            unit = result['unit_name']
            subunit = result['subunit_name']

            if subunit:
                results_list.append(subunit + ', ' + unit)
            else:
                results_list.append(unit)
    else:
        query = f'SELECT {column} FROM \
            person_{entity_type} pe \
            JOIN {entity_type} AS e \
            ON pe.fk_{entity_type}_id = e.{entity_type}_id \
            WHERE fk_person_id = {person_id};'
    
        if entity_id != 0:
            query = query[:-1] + f' AND fk_{entity_type}_id = {entity_id};'
        
        try:
            results = execute(query, 'fetchall')
        except:
            print("Query failed:", query)

        for result in results:
            for i in range(len(result)):
                if isinstance(result[i], str):
                    results_list.append(result[i].replace("'", ''))
                else:
                    results_list.append(result[i])

    return results_list


def get_person_units(entity_type=str, public_id=str) -> list:
    query = f'SELECT * FROM vw_person_units \
            WHERE {entity_type}_public_id = "{public_id}"'
    results = []

    try:
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    person_units = []
    if results:
        fields = ['person_public_id', 'person_name', 'person_email', 
                  'support_type', 'photo_url', 'unit_id', 'unit_public_id', 
                  'unit_name', 'parent_unit_public_id', 'parent_unit_name']
        
        for result in results: 
            result_dict = {}
            i = 0
            for field in fields:
                if field == 'support_type':
                    if result[i] == "Formal":
                       result_dict[field] = "Formal Supporter"
                    elif result[i] == "Informal":
                       result_dict[field] = "Informal Supporter"
                    else:
                       result_dict[field] = "Collaborator"
                else:
                    result_dict[field] = result[i]
                i += 1

            person_units.append(result_dict)

    return person_units


def get_person_support(person_id) -> dict:
    person_support = {'areas': {}, 'methods': {}, 'tools': {}}
    query = f'SELECT * FROM vw_person_support WHERE person_id = {person_id};'
    results = pd.DataFrame([])

    try:
        results = pd.DataFrame(execute(query, 'fetchall'))
    except:
        print("Query failed:", query)
    
    if not results.empty:
        results.columns = ['person_id', 'first_name', 'last_name', 'support_type', 'photo_url'
                            'area_id', 'area_name', 'area_proficiency_id',
                            'area_proficiency', 'area_notes', 
                            'method_id', 'method_name', 'method_proficiency_id', 
                            'method_proficiency', 'method_notes', 
                            'tool_id', 'tool_name', 'tool_type', 'tool_website', 
                            'tool_proficiency_id', 'tool_proficiency', 
                            'tool_notes', 'campus']
          
        for index, row in results.iterrows():
            area = row['area_name']
            method = row['method_name']
            tool = row['tool_name']
            area_proficiency = row['area_proficiency']
            method_proficiency = row['method_proficiency']
            tool_proficiency = row['tool_proficiency']
            area_notes = get_markdown(row['area_notes'])
            method_notes = get_markdown(row['method_notes'])
            tool_notes = get_markdown(row['tool_notes'])
            tool_type = row['tool_type']
            tool_website = row['tool_website']

            if area and area not in person_support['areas']:
                person_support['areas'][area] = {'proficiency': area_proficiency,
                                                 'notes': area_notes}
            if method and method not in person_support['methods']:
                person_support['methods'][method] = {'proficiency': method_proficiency,
                                                     'notes': method_notes}
            if tool and tool not in person_support['tools']:
                person_support['tools'][tool] = {'tool_type': tool_type,
                                                 'website': tool_website,
                                                 'proficiency': tool_proficiency,
                                                 'notes': tool_notes}
                

    return person_support


""" Unit Get Functions """

def get_unit(public_id):
    # Get unit information
    query = f'SELECT * FROM vw_units WHERE public_id = "{public_id}";'
    results = []

    try:
        results = execute(query, 'first')
    except:
        print("Query failed:", query)

    unit = None
    is_subunit = False

    # Check if unit or subunit by parent unit value
    if results:
        unit = db_session.query(Unit).filter_by(public_id=public_id).first()
        if results[10]:
            is_subunit = True

    return unit, is_subunit
    

def get_unit_subunits(entity_type=str, public_id=str) -> list:
    if entity_type == 'unit':
        fields = ['public_id', 'unit_name', 'unit_type']
        query = f'SELECT DISTINCT {", ".join(fields)} FROM vw_units \
            WHERE parent_unit_public_id = "{public_id}"'
    elif entity_type == 'subunit':
        fields = ['parent_unit_public_id', 'parent_unit_name']
        query = f'SELECT DISTINCT {", ".join(fields)} FROM vw_units \
                WHERE public_id = "{public_id}"'
        
    results = []
    try:
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    unit_subunits = []
    if results:        
        for result in results: 
            result_dict = {}
            i = 0
            for field in fields:
                if field == 'description':
                    result_dict[field] = get_markdown(result[i])
                else:
                    result_dict[field] = result[i]
                i += 1

            unit_subunits.append(result_dict)

    return unit_subunits


def get_unit_by_name(unit_name=str) -> Unit:
    # Get unit information
    query = f'SELECT * FROM vw_units WHERE unit_name = "{unit_name}";'
    results = []

    try:
        results = execute(query, 'first')
    except:
        print("Query failed:", query)
    
    # Check if unit or subunit by parent unit value
    unit = None

    if results:
        # Check if it's in the unit or subunit tables and return the first
        unit = db_session.query(Unit).filter_by(unit_name=unit_name).first()

    return unit


def get_all_units():
    query = "SELECT DISTINCT unit_name FROM vw_units;"

    return execute(query, 'fetchall')


def get_unit_support(entity_type=str, public_id=str) -> list:
    query = f'SELECT DISTINCT * FROM vw_unit_support \
            WHERE fk_public_id = "{public_id}" \
            AND {entity_type}_id IS NOT NULL;'
    results = []

    try:
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    unit_support = []
    if results:
        fields = ['fk_public_id', 'unit_id', 'unit_name', 'area_id', 
                  'area_name', 'resource_id', 'resource_name', 'resource_type', 
                  'resource_website', 'resource_notes']
        
        for result in results: 
            result_dict = {}
            i = 0
            for field in fields:
                if field == 'resource_notes':
                    result_dict[field] = get_markdown(result[i])
                else:
                    result_dict[field] = result[i]
                i += 1

            unit_support.append(result_dict)

    return unit_support


def get_unit_funding(entity_type, public_id=str):
    query = f'SELECT * FROM vw_funding \
        WHERE {entity_type}_public_id = "{public_id}"'
    results = []

    try:
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    unit_funding = []
    if results:
        fields = ['funding_public_id', 'funding_id', 'funding_name', 
                  'funding_type', 'payment_type', 'amount', 'career_level', 
                  'duration', 'frequency', 'web_address', 'unit_public_id', 
                  'unit_name', 'campus', 'added_by', 'last_modified']
        
        for result in results: 
            result_dict = {}
            i = 0
            for field in fields:
                result_dict[field] = result[i]
                i += 1

            unit_funding.append(result_dict)

    return unit_funding


""" General Get Functions """

def get_address(building_name=str, room_number=str, street_address=str, 
                address_2=str, city=str, state=str, zipcode=str, campus=str):
    address = []
    
    try:
        address = Address.query.filter_by(building_name=building_name).\
            filter_by(room_number=room_number).filter_by(street_address=street_address).\
            filter_by(address_2=address_2).filter_by(city=city).filter_by(state=state).\
            filter_by(zipcode=zipcode).filter_by(campus=campus).first()
    except:
        print("Address query failed")
    
    if address:
        return True, address
    else:
        return False, None


def get_entity_address(public_id):
    query = f"SELECT * FROM vw_addresses WHERE public_id = '{public_id}';"
    results = []

    try:
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    addresses = []
    if results:
        fields = ['entity_id', 'public_id', 'entity_name', 'address_id', 
                  'building_name', 'room_number', 'street_address', 'address_2', 
                  'city', 'state', 'zipcode', 'campus', 'added_by', 'date_added']
        
        for result in results: 
            result_dict = {}
            i = 0
            for field in fields:
                result_dict[field] = result[i]
                i += 1

            addresses.append(result_dict)
        
    return addresses


def get_field_list(query):
    results = []
    try:
        result = list(zip(*db_session.execute(text(query)).fetchall()))[0]
    except:
        print("Query failed:", query)
    return results


def get_markdown(input=str) -> str:
    if input:
        text = input
        # Ensure hyperlink prefix
        # pattern for Markdown hyperlink
        pattern = r'\[[^!?\s]*\]\([^!?\s]*\)'
        
        for match in re.finditer(pattern, text):
            hyperlink = match[0]
            # Check if hyperlink is not prefixed
            if re.match(r'\[[^!?\s]*\]\([^http][^!?\s]*', hyperlink) or \
                re.match(r'\[[^!?\s]*\]\([^www.][^!?\s]*', hyperlink) or \
                re.match(r'\[[^!?\s]*\]\([^\\][^!?\s]*', hyperlink):
                prefixed_hyperlink = hyperlink.replace("(", "(//")
                text = text.replace(hyperlink, prefixed_hyperlink)

        # Strip enclosing paragraph marks, <p> ... </p>, which markdown() forces
        text = re.sub("(^<P>|</P>$)", "", markdown(text), flags=re.IGNORECASE)

        # Add target
        text = text.replace("<a href", "<a target='_blank' href")

        return text
    return input
