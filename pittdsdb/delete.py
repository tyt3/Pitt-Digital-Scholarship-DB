from flask import Blueprint, request, jsonify, flash
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from flask_restful import Api, Resource
from functools import wraps
from .database import db_session, engine
from .models import *
from .schemas import *


def delete_affiliations(person_id):
    db_session.execute(f'DELETE FROM person_affiliation \
                       WHERE fk_person_id = {person_id };')