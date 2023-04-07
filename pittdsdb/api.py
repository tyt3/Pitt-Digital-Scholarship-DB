"""Module for Views"""
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from .database import db_session
from .models import *


"""Create API Blueprint"""
api_bp = Blueprint('api_bp', __name__)


"""Get Methods"""
@api_bp.route('/getPerson')
def getPerson():
    args = request.args
    name = args.get('name')

    return name


"""Add Methods"""
@api_bp.route('/addMethod', methods=['GET','POST'])
def addMethod():
    args = request.args
    method_name = args.get('name')

    new_method = models.Method(method_name)

    db_session.add(new_method)
    db_session.commit()

    return {'method_name': method_name}, 200
