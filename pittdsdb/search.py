from flask import Blueprint, request, jsonify
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from functools import wraps
import pandas as pd
from .database import db_session
from .models import *
from .schemas import *


"""" Search Functions """

def search_person(first_name=str, last_name=str, title=str, support_type=list, 
                  campus=list, area=list, method=list, tool=list, tool_type=list):
    sql = f'SELECT DISTINCT public_id, p.first_name, p.last_name, title, email, p.photo_url \
        FROM person AS p \
        JOIN vw_person_support AS ps ON p.person_id = ps.person_id'
    empty = True

    if first_name:
        sql += f' WHERE p.first_name LIKE "{first_name}"'
        empty = False

    if last_name:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'p.last_name LIKE "{last_name}"'
        empty = False

    if title:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'p.title = "{title}"'
        empty = False

    if support_type:
        support_type = ",".join("'" + str(x) + "'" for x in support_type)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'p.support_type = {support_type}'
        print(sql)
        empty = False

    if campus:
        campus = ",".join("'"+str(x)+"'" for x in campus)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'campus IN ({campus})'
        empty = False

    if area:
        area = ",".join("'" + str(x) + "'" for x in area)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'area_name IN ({area})'
        empty = False

    if method:
        method = ",".join("'" + str(x) + "'" for x in method)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'method_name IN ({method})'
        empty = False

    if tool:
        tool = ",".join("'" + str(x) + "'" for x in tool)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'tool_name IN ({tool})'
        empty = False

    if tool_type:
        tool_type = ",".join("'" + str(x) + "'" for x in tool_type)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'tool_type IN ({tool_type})'
        empty = False

    # API results
    results = db_session.execute(text(sql + ';')).fetchall()
    
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
    sql = f'SELECT DISTINCT u.public_id, u.unit_name, u.unit_type, u.web_address \
          FROM vw_units AS u'
    empty = True
    
    if area or resource_type:
        sql += f' JOIN vw_unit_support AS us ON u.public_id = us.fk_public_id'

    if offers_funding:
        sql += f' JOIN vw_funding AS uf ON u.public_id = uf.fk_public_id'

    if unit_name:
        sql += f' WHERE unit_name LIKE "{unit_name}"'
        empty = False

    if unit_type:
        unit_type = ",".join("'"+str(x)+"'" for x in unit_type)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f' unit_type IN ({unit_type})'
        empty = False

    if campus:
        campus = ",".join("'"+str(x)+"'" for x in campus)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f' campus IN ({campus})'
        empty = False

    if area:
        area = ",".join("'"+str(x)+"'" for x in area)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f' area_name IN ({area})'
        empty = False
    
    if resource_type:
        resource_type = ",".join("'"+str(x)+"'" for x in resource_type)
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f' resource_type IN ({resource_type})'
        empty = False

    # API results
    results = db_session.execute(text(sql + ';')).fetchall()
    
    # Frontend results
    search_results = []

    if results:
        # Frontend results
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
    sql = f'SELECT DISTINCT * FROM vw_funding'
    empty = True

    if funding_name:
        sql += f' WHERE unit_name LIKE "{funding_name}"'
        empty = False

    if funding_type:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        funding_type = ",".join("'"+str(x)+"'" for x in funding_type)
        sql += f'funding_type IN ({funding_type})'
        empty = False

    if duration:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        duration = ",".join("'"+str(x)+"'" for x in duration)
        sql += f'duration IN ({duration})'
        empty = False

    if frequency:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        frequency = ",".join("'"+str(x)+"'" for x in frequency)
        sql += f'frequency IN ({frequency})'
        empty = False

    if payment_type:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        payment_type = ",".join("'"+str(x)+"'" for x in payment_type)
        sql += f'payment_type IN ({payment_type})'
        empty = False

    if min_amount:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'payment_amount >= {min_amount} OR payment_amount IS NULL'
        empty = False

    if max_amount:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        sql += f'payment_amount >= {max_amount} OR payment_amount IS NULL'
        empty = False

    if career_level:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        career_level = ",".join("'"+str(x)+"'" for x in career_level)
        sql += f'career_level IN ({career_level})'
        empty = False
    
    if campus:
        if empty:
            sql += f' WHERE '
        else:
            sql += f' AND '
        campus = ",".join("'"+str(x)+"'" for x in campus)
        sql += f'campus IN ({campus})'
        empty = False

    # API results
    results = db_session.execute(text(sql + ';')).fetchall()
    
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
    