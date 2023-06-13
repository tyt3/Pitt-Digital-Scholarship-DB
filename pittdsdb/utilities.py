from flask import flash
from flask_login import current_user
from http.client import HTTPException
import hashlib
import hmac
import re
from .database import db_session, engine
from .models import *


def check_entity(table, entity_type, entity_id):
    prefix = ""
    if table != "vw_person_support" and table != "vw_unit_support":
        prefix = "fk_"

    query = f"SELECT * FROM { table } \
            WHERE { prefix }{entity_type}_id = {entity_id};"
    
    results = None
    try:
        results = db_session.execute(text(query)).first()
    except:
        print("Query failed:", query)

    if results:
        return True
    return False


def check_relation(table, entity_1_type, entity_1_id, entity_2_type, entity_2_id):
    prefix = ""
    if table != "vw_person_support" and table != "vw_unit_support":
        prefix = "fk_"

    query = f"SELECT * FROM { table } \
            WHERE { prefix }{entity_1_type}_id = {entity_1_id} \
            AND { prefix }{entity_2_type}_id = {entity_2_id};"
    
    results = None
    try:
        results = execute(query, 'first')
    except:
        print("Query failed:", query)

    if results:
        return True
    return False


def check_unit_subunit(unit_name, parent_unit_name):
    query = f'SELECT * FROM vw_units \
            WHERE unit_name = "{ unit_name }" \
            AND parent_unit_name = "{parent_unit_name}"'
    results = None
    
    try:   
        results = execute(query, 'fetchall')
    except:
        print("Query failed:", query)

    if results:
        return True
    return False


def execute(query=str, method=None):
    query = re.sub(r'[^\S\r\n\t]{2,}', ' ', query)

    if method == 'fetchall':
        return db_session.execute(text(query)).fetchall()
    elif method == 'fetchone':
        return db_session.execute(text(query)).fetchone()
    elif method == 'first':
        return db_session.execute(text(query)).first()
    else:
        db_session.execute(text(query))


def list_intersection(list1=list, list2=list):
    list3 = [value for value in list1 if value in list2]
    return list3


def log_modification(description, timestamp):
    description = re.sub(r'[^\S\r\n\t]{2,}', ' ', description)
    modification = Modification(modification=description,
                                modified_by=current_user.user_id,
                                modification_date=timestamp)
    
    # Add modification log to database
    db_session.add(modification)
    db_session.commit()


def now():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def verify_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)
