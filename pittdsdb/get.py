from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
import pandas as pd
from .database import db_session, engine
from .models import *
from .schemas import *



def search_person(first_name, last_name, title, support_type, campus, area, method, tool):
    sql = f'SELECT DISTINCT public_id, first_name, last_name, title, email FROM person '
    empty = True

    if campus:
        campus = campus.split(',')
        campus = ",".join("'"+str(x)+"'" for x in campus)
        sql += f'JOIN person_address pa ON person.person_id = pa.fk_person_id JOIN address a ON pa.fk_address_id = a.address_id '

    if area:
        area = area.split(',')
        area = ",".join("'" + str(x) + "'" for x in area)
        sql += f'JOIN person_area parea ON person.person_id = parea.fk_person_id JOIN area ON parea.fk_area_id = area.area_id '

    if method:
        method = method.split(',')
        method = ",".join("'" + str(x) + "'" for x in method)
        sql += f'JOIN person_method pm ON person.person_id = pm.fk_person_id JOIN method m ON pa.fk_method_id = m.method_id '

    if tool:
        tool = tool.split(',')
        tool = ",".join("'" + str(x) + "'" for x in tool)
        sql += f'JOIN person_tool pt ON person.person_id = pt.fk_person_id JOIN tool t ON pt.fk_tool_id = t.tool_id '

    sql += f'WHERE '
    if first_name:
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
        sql += f'title = "{title}"'
        empty = False
    if support_type:
        if not empty:
            sql += f' AND '
        sql += f'support_type = "{support_type}"'
        empty = False
    if campus:
        if not empty:
            sql += f' AND '
        sql += f'a.campus IN ({campus})'
        empty = False

    if area:
        if not empty:
            sql += f' AND '
        sql += f'area.area_name IN ({area})'
        empty = False

    if method:
        if not empty:
            sql += f' AND '
        sql += f'm.method_name IN ({method})'
        empty = False

    if tool:
        if not empty:
            sql += f' AND '
        sql += f't.tool_name IN ({tool})'
        empty = False

    if empty:
        return "Please enter at least one parameter for your query from \
                id, first_name, last_name, support_type, campus"

    else:
        # API results
        results = db_session.execute(text(sql + ';')).fetchall()
        
        # Frontend results
        search_results = []

        if results:
            # Frontend results
            results_df = pd.DataFrame(results)
            results_df.columns = ['public_id', 'first_name', 'last_name', 'title', 'email']

            for index, row in results_df.iterrows():
                public_id = row['public_id']
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                title = row['title']

                search_result = {'public_id': public_id,
                                 'first_name': first_name,
                                 'last_name': last_name,
                                 'email': email,
                                 'title:': title}

                search_results.append(search_result)


        return results, search_results


def get_person_relations(person_id=int, column=str, entity=str, entity_id=0):
    query = None
    if entity == "unit":
        query = f'SELECT subunit_name, unit_name FROM vw_person_units \
        WHERE person_id = { person_id };'    
    else:
        query = f'SELECT { column } FROM \
            person_{ entity } pe \
            JOIN { entity } AS e \
            ON pe.fk_{ entity }_id = e.{ entity }_id \
            WHERE fk_person_id = { person_id };'
    
    if entity_id != 0:
        query = query[:-1] + f' AND fk_{ entity }_id = { entity_id };'

    results = db_session.execute(text(query)).fetchall()
    results_list = []

    for result in results:
        if entity == "unit":
            subunit = result[0]
            unit = result[1]
            if subunit:
                results_list.append(subunit + ', ' + unit)
            else:
                results_list.append(unit)
        else:
            for i in range(len(result)):
                if isinstance(result[i], str):
                    results_list.append(result[i].replace("'", ''))
                else:
                    results_list.append(result[i])

    return results_list


def get_person_support(person_id):
    person_support = {'areas': {}, 'methods': {}, 'tools': {}}


    results = pd.DataFrame(db_session.execute(text(f'SELECT * FROM vw_person_support \
                                 WHERE person_id = { person_id };')).fetchall())
    
    if not results.empty:
        results.columns = ['person_id', 'first_name', 'last_name', 'support_type',
                            'area_id', 'area_name', 'area_proficiency_id',
                            'area_proficiency', 'area_notes', 'method_id', 
                            'method_name', 'method_proficiency_id', 
                            'method_proficiency',  'method_notes', 'tool_id', 
                            'tool_name', 'tool_proficiency_id', 'tool_website', 
                            'tool_proficiency', 'tool_notes', 'campus']
          
        for index, row in results.iterrows():
            area = row['area_name']
            method = row['method_name']
            tool = row['tool_name']
            area_proficiency = row['area_proficiency']
            method_proficiency = row['method_proficiency']
            tool_proficiency = row['tool_proficiency']
            area_notes = row['area_notes']
            method_notes = row['method_notes']
            tool_notes = row['tool_notes']
            tool_website = row['tool_website']

            if area and area not in person_support['areas']:
                person_support['areas'][area] = {'proficiency': area_proficiency,
                                                 'notes': area_notes}
            if method and method not in person_support['methods']:
                person_support['methods'][method] = {'proficiency': method_proficiency,
                                                     'notes': method_notes}
            if tool and tool not in person_support['tools']:
                person_support['tools'][tool] = {'website': tool_website,
                                                     'proficiency': tool_proficiency,
                                                     'notes': tool_notes}
                
    print(person_support['areas'])

    return person_support
