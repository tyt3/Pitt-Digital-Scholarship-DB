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


def get_person_relations(column, entity):
    results = db_session.execute(f'SELECT { column } FROM \
                                            person_{ entity } pe \
                                            JOIN { entity } AS e \
                                            ON pe.fk_{ entity }_id = e.{ entity }_id').fetchall()
    results_list = []
    for result in results:
        for i in range(len(result)):
            if isinstance(result[i], str):
                results_list.append(result[i].replace("'", ''))
            else:
                results_list.append(result[i])

    return results_list


def get_person_support(person_id):
    person_support = {}

    results = pd.DataFrame(db_session.execute(f'SELECT * FROM vw_person_support \
                                 WHERE person_id = { person_id };').fetchall())
    results.columns = ['person_id', 'first_name', 'last_name', 'support_type', 
                       'area_id', 'area_name', 'method_id', 'method_name', 
                       'method_proficiency_id', 'method_proficiency', 'tool_id', 
                       'tool_name', 'tool_proficiency_id', 'tool_proficiency', 
                       'campus']
    
    for index, row in results.iterrows():
        area = row['area_name']
        method = row['method_name']
        tool = row['tool_name']
        method_proficiency = row['method_proficiency']
        tool_proficiency = row['tool_proficiency']

        if area not in person_support: # no area, method, or tool
            if method and tool:
                person_support[area] = { method: {'proficiency': method_proficiency,
                                                  'tools': {tool: tool_proficiency}}}
            elif method:
                person_support[area] = { method: {'proficiency': method_proficiency,
                                                  'tools': {}}}
            else:
                person_support[area] = {}
        elif method and method not in person_support[area]: # area, method, no tool
            person_support[area][method] = {'proficiency': method_proficiency,
                                                  'tools': {}}
        elif tool and tool not in person_support[area][method]['tools']: # area, method, tool
            person_support[area][method]['tools'][tool] = tool_proficiency

    return person_support