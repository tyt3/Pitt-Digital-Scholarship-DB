from flask import Blueprint, request, jsonify
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
from .database import db_session
from .models import *
from .schemas import *


def search_person(person_id=int, first_name="", last_name="", title="", support_type=[], 
                  campus=[], areas=[], methods=[], tools=[]):
    sql = f'SELECT person_id FROM vw_person_support WHERE '
    empty = True

    if person_id:
        sql += f'person_id = "{person_id}"' 
        empty = False
    if first_name:
        if not empty:
            sql += f' AND '
        sql += f'first_name LIKE "{first_name}"' 
        empty = False
    if last_name:
        if not empty:
            sql += f' AND '
        sql += f'last_name LIKE "{last_name}"'
        empty = False
    if title:
        if not empty:
            sql += f' AND '
        sql += f'title LIKE "{title}"'
        empty = False
    if support_type:
        support_type_str = str(support_type).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'support_type IN "{support_type_str}"'
        empty = False
    if campus:
        campus_str = str(campus).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'campus IN "{campus_str}"'
        empty = False
    if areas:
        area_str = str(areas).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'area_name IN "{area_str}"'
        empty = False
    if methods:
        methods_str = str(methods).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'method_name IN "{methods_str}"'
        empty = False
    if tools:
        tools_str = str(tools).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'tool_name IN "{tools_str}"'
        empty = False
    
    if empty:
        return "Please enter at least one parameter for your query from \
            ID, First Name, Last Name, Support Type, Campus, \
            Supported Areas, Supported Methods, Supported Tools"
    else:
        result = db_session.execute(text(sql + ';')).fetchall()

    person_list = Person.query.filter_by(Person.person_id.in_(result)).fetchall()

    return person_schema.jsonify(person_list)


def search_unit(unit_id=int, unit_name="", areas=[], resources=[], campus=[], 
                is_lab=False):
    sql = f'SELECT * FROM vw_person_support WHERE '
    empty = True

    if unit_id:
        sql += f'unit_id = "{unit_id}"' 
        empty = False
    if unit_name:
        if not empty:
            sql += f' AND '
        sql += f'first_name LIKE "{unit_name}"' 
        empty = False
    if campus:
        campus_str = str(campus).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'campus IN "{campus_str}"'
        empty = False
    if areas:
        areas_str = str(areas).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'area_name IN "{areas_str}"'
        empty = False
    if resources:
        resources_str = str(resources).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'resource_name IN "{resources_str}"'
        empty = False
    if is_lab:
        if not empty:
            sql += f' AND '
        sql += 'entity_type = "Lab"'
        empty = False
    if empty:
        return "Please enter at least one parameter for your query from \
            ID, Name, Supported Areas, Supported Resources, and Campus"
    else:
        result = db_session.execute(text(sql + ';')).fetchall()
        result = list(set(list(zip(*result))[0]))

    entity_list = []
    # How best to schematize multiple entities?
    # Create an entities view and then schematize it with Marshmallow?

    return entity_list


def search_funding(funding_id, funding_name, funding_type, payment_type, 
                   min_amount, max_amount, career_level, duration, frequency, 
                   campus):
    sql = f'SELECT person_id FROM vw_person_support WHERE '
    empty = True

    if funding_id:
        sql += f'funding_id = "{funding_id}"' 
        empty = False
    if funding_name:
        if not empty:
            sql += f' AND '
        sql += f'funding_name LIKE "{funding_name}"' 
        empty = False
    if funding_type:
        funding_type_str = str(funding_type).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'funding_type IN "{funding_type_str}"'
        empty = False
    if payment_type:
        payment_type_str = str(payment_type).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'payment_type IN "{payment_type_str}"'
        empty = False
    if min_amount:
        if not empty:
            sql += f' AND '
        sql += f'amount >= {min_amount}' 
        empty = False
    if max_amount:
        if not empty:
            sql += f' AND '
        sql += f'amount <= {max_amount}' 
        empty = False
    if career_level:
        career_level_str = str(career_level).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'career_level IN "{career_level_str}"'
        empty = False
    if duration:
        duration_str = str(duration).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'duration IN "{duration_str}"'
        empty = False
    if frequency:
        frequency_str = str(frequency).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'frequency IN "{frequency_str}"'
        empty = False
    if campus:
        campus_str = str(campus).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'campus IN "{campus_str}"'
        empty = False
    
    if empty:
        return "Please enter at least one parameter for your query from \
            ID, First Name, Last Name, Support Type, Campus, \
            Supported Areas, Supported Methods, Supported Tools"
    else:
        result = db_session.execute(text(sql + ';')).fetchall()

    person_list = Person.query.filter_by(Person.person_id.in_(result)).fetchall()

    return person_schema.jsonify(person_list)
