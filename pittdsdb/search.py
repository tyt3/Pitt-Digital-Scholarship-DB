from flask import Blueprint, request, jsonify
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
import pandas as pd
from .database import db_session
from .models import *
from .schemas import *
from .utilities import *


"""" Search Functions """

def search_person(first_name=str, last_name=str, title=str, support_type=list, 
                  campus=list, area=list, method=list, tool=list, tool_type=list):
    query = f'SELECT DISTINCT public_id, p.first_name, p.last_name, title, email, p.photo_url \
            FROM person AS p JOIN vw_person_support AS ps ON p.person_id = ps.person_id'
    empty = True
    base_results = area_results = method_results = tool_results = None
    results = []

    if first_name:
        query += f' WHERE p.first_name LIKE "%{first_name}%"'
        empty = False

    if last_name:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'p.last_name LIKE "%{last_name}%"'
        empty = False

    if title:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'p.title LIKE "%{title}%"'
        empty = False

    if support_type:
        support_type = ",".join("'" + str(x) + "'" for x in support_type)
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'p.support_type = {support_type}'
        empty = False

    if campus:
        campus = ",".join("'"+str(x)+"'" for x in campus)
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'campus IN ({campus})'
        empty = False
    
    try:
        base_results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    if base_results:
        results = base_results

    if area:
        area = ",".join("'" + str(x) + "'" for x in area)
        # Add area condition to query
        if empty:
            area_query = query + f' WHERE area_name IN ({area})'
        else:
            area_query = query + f' AND area_name IN ({area})'
        # Execute query
        try:
            area_results = execute(area_query, 'fetchall')
        except:
            print("Query failed:", area_query)
        # Update results
        if base_results:
            results = list_intersection(results, area_results)
        else:
            results = area_results

    if method:
        method = ",".join("'" + str(x) + "'" for x in method)
        # Add method condition to query
        if empty:
            method_query = query + f' WHERE method_name IN ({method})'
        else:
            method_query = query + f' AND method_name IN ({method})'
        # Execute query
        try:
            method_results = execute(method_query, 'fetchall')
        except:
            print("Query failed:", method_query)
        # Update results
        if base_results or area_results:
            results = list_intersection(results, method_results)
        else:
            results = method_results

    if tool:
        tool = ",".join("'" + str(x) + "'" for x in tool)
        # Add tool condition to query
        if empty:
            tool_query = query + f' WHERE tool_name IN ({tool})'
        else:
            tool_query = query + f' AND tool_name IN ({tool})'
        # Execute query
        try:
            tool_results = execute(tool_query, 'fetchall')
        except:
            print("Query failed:", tool_query)
        # Update results
        if base_results or area_results or method_results:
            results = list_intersection(results, tool_results)
        else:
            results = tool_results

    if tool_type:
        tool_type = ",".join("'" + str(x) + "'" for x in tool_type)
        # Add tool type condition to query
        if empty:
            tool_type_query = query + f' WHERE tool_type IN ({tool_type})'
        else:
            tool_type_query = query + f' AND tool_type IN ({tool_type})'
        # Execute query
        try:
            tool_type_results = execute(tool_type_query, 'fetchall')
        except:
            print("Query failed:", tool_type_query)
        # Update results
        if base_results or area_results or method_results or tool_results:
            results = list_intersection(results, tool_type_results)
        else:
            results = tool_type_results
    
    # Frontend results
    search_results = []

    if results:
        # Frontend results
        results_df = pd.DataFrame(results)
        results_df.columns = ['public_id', 'first_name', 'last_name', 'title', 'email', 'photo_url']

        for index, row in results_df.iterrows():
            public_id = row['public_id']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            title = row['title']
            photo_url = row['photo_url']

            search_result = {'public_id': public_id,
                             'first_name': first_name,
                             'last_name': last_name,
                             'email': email,
                             'title:': title,
                             'photo_url': photo_url}

            search_results.append(search_result)

    return results, search_results


def search_unit(unit_name=str, unit_type=list, campus=list, area=list, 
                resource_type=list, offers_funding=bool):
    query_base = f'SELECT DISTINCT u.public_id, u.unit_name, u.unit_type, u.web_address \
          FROM vw_units AS u'
    query = query_base
    empty = True
    results = []
    base_results = area_results = resource_results = None

    if area or resource_type:
        query += f' JOIN vw_unit_support AS us ON u.public_id = us.fk_public_id'
    
    if offers_funding:
        query += f' JOIN vw_funding AS uf ON u.public_id = uf.unit_public_id'
    
    if unit_name:
        query += f' WHERE u.unit_name LIKE "%{unit_name}%"'
        empty = False

    if unit_type:
        unit_type = ",".join("'"+str(x)+"'" for x in unit_type)
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f' u.unit_type IN ({unit_type})'
        empty = False

    if campus:
        campus = ",".join("'"+str(x)+"'" for x in campus)
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f' u.campus IN ({campus})'
        empty = False
    
    try:
        base_results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    if base_results:
        results = base_results

    if area:
        area = ",".join("'"+str(x)+"'" for x in area)
        area_query = ''
        if empty:
            area_query = query + f' WHERE area_name IN ({area})'
        else:
            area_query = query + f' AND area_name IN ({area})'
        
        try:
            area_results = execute(area_query, 'fetchall')
        except:
            print("Query failed:", area_query)

        if base_results:
            results = list_intersection(results, area_results)
        else:
            results = area_results
    
    if resource_type:
        resource_type = ",".join("'"+str(x)+"'" for x in resource_type)
        resource_query = ''
        if empty:
            resource_query = query + f' WHERE resource_type IN ({resource_type})'
        else:
            resource_query = query + f' AND resource_type IN ({resource_type})'
        
        try:
            resource_results = execute(resource_query, 'fetchall')
        except:
            print("Query failed:", resource_query)

        if base_results or area_results:
            results = list_intersection(results, resource_results)
        else:
            results = resource_results

    # Frontend results
    search_results = []

    if results:
        results_df = pd.DataFrame(results)
        results_df.columns = ['public_id', 'unit_name', 'unit_type', 
                              'web_address']

        for index, row in results_df.iterrows():
            public_id = row['public_id']
            unit_name = row['unit_name']
            unit_type = row['unit_type']
            web_address = row['web_address']

            search_result = {'public_id': public_id,
                             'unit_name': unit_name,
                             'unit_type': unit_type,
                             'web_address': web_address}

            search_results.append(search_result)

    return results, search_results


def search_funding(funding_name=str, funding_type=list, duration=list, 
                   frequency=list, payment_type=list, min_amount=float, 
                   max_amount=float, career_level=list, campus=list):
    query = f'SELECT DISTINCT * FROM vw_funding'
    empty = True
    results = []

    if funding_name:
        query += f' WHERE unit_name LIKE "%{funding_name}%"'
        empty = False

    if funding_type:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        funding_type = ",".join("'"+str(x)+"'" for x in funding_type)
        query += f'funding_type IN ({funding_type})'
        empty = False

    if duration:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        duration = ",".join("'"+str(x)+"'" for x in duration)
        query += f'duration IN ({duration})'
        empty = False

    if frequency:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        frequency = ",".join("'"+str(x)+"'" for x in frequency)
        query += f'frequency IN ({frequency})'
        empty = False

    if payment_type:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        payment_type = ",".join("'"+str(x)+"'" for x in payment_type)
        query += f'payment_type IN ({payment_type})'
        empty = False

    if min_amount:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'payment_amount >= {min_amount} OR payment_amount IS NULL'
        empty = False

    if max_amount:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        query += f'payment_amount >= {max_amount} OR payment_amount IS NULL'
        empty = False

    if career_level:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        career_level = ",".join("'"+str(x)+"'" for x in career_level)
        query += f'career_level IN ({career_level})'
        empty = False
    
    if campus:
        if empty:
            query += f' WHERE '
        else:
            query += f' AND '
        campus = ",".join("'"+str(x)+"'" for x in campus)
        query += f'campus IN ({campus})'
        empty = False

    # API results
    try:
        results = db_session.execute(text(query + ';')).fetchall()
    except:
        print("Query failed:", query)
    
    # Frontend results
    search_results = []

    if results:
        results_df = pd.DataFrame(results)
        results_df.columns = ['funding_public_id',
                              'funding_id', 'funding_name', 'funding_type', 
                              'payment_type', 'payment_amount', 'career_level', 
                              'duration', 'frequency', 'web_address', 
                              'unit_public_id', 'unit_name', 'campus', 
                              'added_by', 'last_modified']

        for index, row in results_df.iterrows():
            public_id = row['funding_public_id']
            funding_name = row['funding_name']
            funding_type = row['funding_type']
            payment_type = row['payment_type']
            payment_amount = row['payment_amount']
            web_address = row['web_address']

            search_result = {'public_id': public_id,
                                'funding_name': funding_name,
                                'funding_type': funding_type,
                                'payment_type': payment_type,
                                'payment_amount': payment_amount,
                                'web_address': web_address}

            search_results.append(search_result)

    return results, search_results
    