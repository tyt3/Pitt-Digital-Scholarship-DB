"""Module for Views"""
from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.sql import text
from flask_restful import Api, Resource
import jwt
from datetime import datetime, timedelta
from .database import db_session
from .models import *
from .schemas import *
from .token_auth import *
from .config import SECRET_KEY
from passlib.hash import sha256_crypt
from .networkdb import *



"""Create API Blueprint"""
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/logon', methods=['GET', 'POST'])
def logon():
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
@token_required
def get_person(current_user):
    args = request.args
    first_name = args.get('first_name')
    last_name = args.get('last_name')
    title = args.get('title')
    support_type = args.get('support_type')
    campus = args.get('campus')
    area = args.get('area')
    method = args.get('method')
    tool = args.get('tool')
    sql = f'SELECT DISTINCT public_id, first_name, last_name FROM person '
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
        results = db_session.execute(text(sql + ';')).fetchall()

    if len(results) > 1:
        return people_schema.jsonify(results)
    else:
        return person_schema.jsonify(results)

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

    return {'area_name': area_name}, 200

@api_bp.route('/update_area', methods=['GET'])
@token_required
def update_area(current_user):
    args = request.args
    name = args.get('name')
    area = Area.query.filter_by(name)
    if area:
        new_name = args.get('new_name')
        update_area_node(area.area_name, new_name)
        area.area_name = new_name
        db_session.commit()
        return {'area_name': new_name}, 200
    return {'Error': 'Area Not exists'}, 404

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

@api_bp.route('/update_method', methods=['GET'])
@token_required
def update_method(current_user):
    args = request.args
    method_name = args.get('name')
    new_name = args.get('new_name')
    method = Area.query.filter_by(method_name=method_name)
    if method:
        update_method_node(method.method_name, new_name)
        method.area_name = new_name
        db_session.commit()
        return {'method_name': new_name}, 200
    return {'Error': 'Method Not exists'}, 404

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