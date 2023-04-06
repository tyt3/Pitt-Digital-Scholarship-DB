"""Module for Views"""
from flask import Blueprint, request, jsonify
from database import db_session
import models


api = Blueprint('api', __name__)

@api.route('/getPerson')
def getPerson():
    args = request.args
    name = args.get('name')

    return name

@api.route('/addMethod')
def addMethod():
    args = request.args
    method_name = args.get('name')

    new_method = models.Method(method_name)

    db_session.add(new_method)
    db_session.commit()

    return {'method_name': method_name}, 200
