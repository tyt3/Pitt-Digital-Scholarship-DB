"""Module for Views"""
from flask import Blueprint, request, jsonify
from sqlalchemy.sql import text
from flask_restful import Api, Resource
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from .database import db_session
from .models import Person, Method
from .schemas import *
from .token_auth import token_required


"""Create API Blueprint"""
api_bp = Blueprint('api_bp', __name__)


"""Get Methods"""
@api_bp.route('/getPerson')
def getPerson():
    args = request.args
    first_name = args.get('first_name')
    last_name = args.get('last_name')
    support_type = args.get('support_type')
    campus = args.get('campus')

    sql = f'SELECT * FROM person WHERE '
    empty = True
    if first_name:
        sql += f'first_name LIKE "{first_name}"' 
        empty = False
    if last_name:
        if not empty:
            sql += f' AND '
        sql += f'last_name LIKE "{last_name}"'
        empty = False
    if support_type:
        if not empty:
            sql += f' AND '
        sql += f'support_type = "{support_type}"'
        empty = False
    
    if empty:
        return "Please enter at least one parameter for your query from \
            id, first_name, last_name, support_type, campus"
       
    else:
        result = db_session.execute(text(sql + ';')).fetchall()

    if len(result) > 1:
        return person_schema.jsonify(result)
    else:
        return people_schema.jsonify(result)

     # result = Person.query.filter_by(first_name=first_name,
        #                                 last_name=last_name)

    


"""Add Methods"""
@api_bp.route('/addPerson')
def addPerson():
    args = request.args
    first_name = args.get('first_name')
    last_name = args.get('last_name')
    title = args.get('title')
    pronouns = args.get('pronouns')
    email = args.get('email')
    web_address = args.get('web_address')
    phone = args.get('phone')
    scheduler_address = args.get('scheduler_address')
    preferred_contact = args.get('preferred_contact')
    support_type = args.get('support_type')
    bio = args.get('bio')
    added_by = args.get('added_by')
    date_added = datetime.now()
    last_modified = date_added
    notes = args.get('notes')

    new_person = Person(first_name, last_name, title, pronouns, email,
                 web_address, phone, scheduler_address, preferred_contact, 
                 support_type, bio, added_by, date_added, last_modified, notes)
    
    db_session.add(new_person)
    db_session.commit()

    return person_schema.jsonify(new_person)


@api_bp.route('/addMethod', methods=['GET','POST'])
def addMethod():
    args = request.args
    method_name = args.get('name')

    new_method = Method(method_name)

    db_session.add(new_method)
    db_session.commit()

    return {'method_name': method_name}, 200
