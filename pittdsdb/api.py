"""Module for Views"""
from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.sql import text
from flask_restful import Api, Resource
from passlib.hash import sha256_crypt
import jwt
from datetime import datetime, timedelta
import pandas as pd
from .database import db_session
from .models import *
from .schemas import *
from .token_auth import *
from .config import SECRET_KEY
from .get import *
from .networkdb import *


"""Create API Blueprint"""
api_bp = Blueprint('api_bp', __name__)


"""Login Method"""
@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if sha256_crypt.verify(auth.password, user.user_password):
        token = jwt.encode({'api_key': user.api_key, 'exp': datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY)
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


"""Get Methods"""
@api_bp.route('/get_person', methods=['GET'])
def get_person():
    args = request.args
    first_name = args.get('first_name')
    last_name = args.get('last_name')
    title = args.get('title')
    support_type = args.get('support_type')
    campus = args.get('campus')
    area = args.get('area')
    method = args.get('method')
    tool = args.get('tool')
    
    results = search_person(first_name, last_name, title, support_type, campus,
    area, method, tool)[0]

    if len(results) > 1:
        return people_schema.jsonify(results)
    else:
        return person_schema.jsonify(results)

@api_bp.route('/get_unit', methods=['GET'])
def get_unit():
    args = request.args
    unit_name = args.get('unit_name')
    campus = args.get('campus')
    area = args.get('area')
    resource = args.get('resource')
    is_lab = args.get('is_lab')
    
    results = search_unit(unit_name, campus, area, resource, is_lab)[0]

    if len(results) > 1:
        return people_schema.jsonify(results)
    else:
        return person_schema.jsonify(results)


@api_bp.route('/get_area', methods=['GET'])
def get_area(area_name):
    area = Area.query.filter_by(area_name=area_name).first()
    if area:
        area_methods = {}
        rows = pd.DataFrame(db_session.execute(text(f'SELECT method_id, method_name FROM method_area ma JOIN method m ON ma.fk_method_id = m.method_id  \
                                        WHERE fk_area_id = {area.area_id};')))
        rows.columns = ['method_id', 'method_name', ]
        for index, row in rows.iterrows():
            method = row['method_name']
            area_methods[method] = get_method(method)
        return {'area_name': area.area_name, 'methods': area_methods}


@api_bp.route('/get_method/<method>', methods=['GET'])
def get_method(method_name):
    method = Method.query.filter_by(method_name=method_name).first()
    method_tools = {}
    rows = pd.DataFrame(db_session.execute(text(f'SELECT tool_id, tool_name FROM method_tool mt JOIN tool t ON mt.fk_tool_id = t.tool_id  \
                                WHERE fk_method_id = {method.method_id};')))
    rows.columns = ['tool_id', 'tool_name', ]
    for index, row in rows.iterrows():
        tool = row['tool_name']
        method_tools[tool] = get_tool(tool)
    return {'method_name': method.method_name, 'tools': method_tools}


@api_bp.route('/get_tool', methods=['GET'])
def get_tool(tool_name):
    tool = Tool.query.filter_by(tool_name=tool_name).first()
    return {'tool_name': tool.tool_name, 'tool_type':tool.tool_type, 'web_address':tool.web_address}


""""Search Methods"""
@api_bp.route('/search_area', methods=['GET'])
def search_area():
    args = request.args
    area_name = args.get('name')
    return get_area(area_name), 200


@api_bp.route('/search_method', methods=['GET'])
def search_method():
    args = request.args
    method_name = args.get('name')
    return get_method(method_name), 200


@api_bp.route('/get_tool', methods=['GET'])
def search_tool():
    args = request.args
    tool_name = args.get('name')
    tool = Tool.query.filter_by(tool_name=tool_name).first()
    return {'area_name': tool.tool_name}, 200


"""Add Methods"""
@api_bp.route('/add_person')
@token_required
def add_person(current_user):
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
    added_by = current_user.get_id()
    date_added = datetime.now()
    last_modified = date_added
    notes = args.get('notes')

    new_person = Person(first_name, last_name, title, pronouns, email,
                 web_address, phone, scheduler_address, preferred_contact, 
                 support_type, bio, added_by, date_added, last_modified, notes)
    
    db_session.add(new_person)
    db_session.commit()

    add_person_node(first_name + " " + last_name, new_person.public_id)
    return person_schema.jsonify(new_person)


@api_bp.route('/add_area', methods=['GET'])
@token_required
def add_area(current_user):
    args = request.args
    area_name = args.get('name')

    new_area = Area(area_name, added_by=current_user.get_id())
    add_area_node(area_name
                  )
    db_session.add(new_area)
    db_session.commit()

    return {'area_name': area_name}, 
    

@api_bp.route('/add_method', methods=['GET'])
@token_required
def add_method(current_user):
    args = request.args
    method_name = args.get('name')

    new_method = Method(method_name, added_by=current_user.get_id())
    add_method_node(method_name)

    db_session.add(new_method)
    db_session.commit()

    return {'method_name': method_name}, 200


@api_bp.route('/add_tool', methods=['GET'])
@token_required
def add_tool(current_user):
    args = request.args
    tool_name = args.get('name')
    tool_type = args.get('type')
    web_address = args.get('name')

    new_tool = Tool(tool_name, tool_type, web_address, added_by=current_user.get_id())
    add_tool_node(tool_name, tool_type)

    db_session.add(new_tool)
    db_session.commit()

    return {'tool_name': tool_name, 'tool_type': tool_type, 'web_address': web_address}, 200


@api_bp.route('/add_resource', methods=['GET'])
@token_required
def add_resource(current_user):
    args = request.args
    resource_name = args.get('name')
    resource_type = args.get('type')
    web_address = args.get('name')

    new_resource = Resource(resource_name, resource_type, web_address, added_by=current_user.get_id())
    add_resource_node(resource_name, resource_type)

    db_session.add(new_resource)
    db_session.commit()

    return {'resource_name': resource_name, 'resource_type': resource_type, 'web_address': web_address}, 200


"""Update Methods"""
@api_bp.route('/update_area', methods=['GET'])
@token_required
def update_area(current_user):
    args = request.args
    name = args.get('name')
    area = Area.query.filter_by(name).first()
    if area:
        new_name = args.get('new_name')
        update_area_node(area.area_name, new_name)
        area.area_name = new_name
        db_session.commit()
        return {'area_name': new_name}, 200
    return {'Error': 'Area Not exists'}, 404


@api_bp.route('/update_method', methods=['GET'])
@token_required
def update_method(current_user):
    args = request.args
    method_name = args.get('name')
    new_name = args.get('new_name')
    method = Method.query.filter_by(method_name=method_name).first()
    if method:
        update_method_node(method.method_name, new_name)
        method.area_name = new_name
        db_session.commit()
        return {'method_name': new_name}, 200
    return {'Error': 'Method Not exists'}, 404


@api_bp.route('/update_tool', methods=['GET'])
@token_required
def update_tool(current_user):
    args = request.args
    name = args.get('name')
    tool = Tool.query.filter_by(name)
    if tool:
        new_name = args.get('new_name')
        if not new_name:
            new_name = tool['resource_name']
        new_type = args.get('new_type')
        if not new_type:
            new_type = tool['resource_type']
        update_tool_node(tool.tool_name, new_name, new_type)
        tool.tool_name = new_name
        tool.tool_type = new_type
        db_session.commit()
        return {'tool_name': new_name}, 200
    return {'Error': 'Tool Not exists'}, 404


@api_bp.route('/update_resource', methods=['GET'])
@token_required
def update_resource(current_user):
    args = request.args
    name = args.get('name')
    resource = Resource.query.filter_by(name)
    if resource:
        new_name = args.get('new_name')
        if not new_name:
            new_name = resource['resource_name']
        new_type = args.get('new_type')
        if not new_type:
            new_type = resource['resource_type']
        update_resource_node(resource.resource_name, new_name, new_type)
        resource.resource_name = new_name
        resource.resource_type = new_type
        db_session.commit()
        return {'resource_name': new_name}, 200
    return {'Error': 'Resource Not exists'}, 404


"""Delete Methods"""
@api_bp.route('/delete_person')
@token_required
def delete_person(current_user):
    if current_user.permission_level != 4:
        args = request.args
        email = args.get('email')
        person = Person.query.filter_by(email=email).first()
        if person:
            public_id = person.public_id
            delete_node('Person', 'public_id', public_id)
            db_session.execute(text(f'DELETE FROM person \
                        WHERE person_id = {person.person_id };'))
            db_session.commit()
            return 'Person Successfully deleted',200
        return {'Error': 'Person Not exists'}, 404
    return {'Error': 'Above Permission Level'}, 403


@api_bp.route('/delete_area')
@token_required
def delete_area(current_user):
    if current_user.permission_level != 4:
        args = request.args
        name = args.get('name')
        area = Area.query.filter_by(area_name=name).first()
        if area:
            delete_node('Area', 'name', name)
            db_session.execute(text(f'DELETE FROM Area \
                        WHERE area_name = {area.area_name };'))
            db_session.commit()
            return 'Area Successfully deleted',200
        return {'Error': 'Area Not exists'}, 404
    return {'Error': 'Above Permission Level'}, 403


@api_bp.route('/delete_method')
@token_required
def delete_method(current_user):
    if current_user.permission_level != 4:
        args = request.args
        name = args.get('name')
        method = Method.query.filter_by(method_name=name).first()
        if method:
            delete_node('Method', 'name', name)
            db_session.execute(text(f'DELETE FROM Method \
                                    WHERE method_name = {method.method_name};'))
            db_session.commit()
            return 'Method Successfully deleted', 200
        return {'Error': 'Method Not exists'}, 404
    return {'Error': 'Above Permission Level'}, 403


@api_bp.route('/delete_tool')
@token_required
def delete_tool(current_user):
    if current_user.permission_level != 4:
        args = request.args
        name = args.get('name')
        tool = Tool.query.filter_by(tool_name=name).first()
        if tool:
            delete_node('Tool', 'name', name)
            db_session.execute(text(f'DELETE FROM Tool \
                                WHERE tool_name = {tool.tool_name};'))
            db_session.commit()
            return 'Tool Successfully deleted', 200
        return {'Error': 'Tool Not exists'}, 404
    return {'Error': 'Above Permission Level'}, 403


@api_bp.route('/delete_resource')
@token_required
def delete_resource(current_user):
    if current_user.permission_level != 4:
        args = request.args
        name = args.get('name')
        resource = Resource.query.filter_by(resource_name=name).first()
        if resource:
            delete_node('Resource', 'name', name)
            db_session.execute(text(f'DELETE FROM Resource \
                                        WHERE resource_name = {resource.resource_name};'))
            db_session.commit()
            return 'Resource Successfully deleted', 200
        return {'Error': 'Resource Not exists'}, 404
    return {'Error': 'Above Permission Level'}, 403