from .database import db_session, engine
from .models import *
from .schemas import *


def manage_person_area(method=str, user_id=int, person_id=int, area_name=str,
                        new_name='', area_proficiency=str, area_notes=''):
    input_list = [method, user_id, person_id, area_name, new_name, 
                  area_proficiency, area_notes, False, None]
    results = None

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonArea", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results


def manage_person_method(method=str, user_id=int, person_id=int, area_name=str,
                          method_name=str, new_name=str, proficiency=str, 
                          notes=str):
    input_list = [method, user_id, person_id, area_name, method_name, new_name, 
                  proficiency, notes, False, None]
    results = None

    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonMethod", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results


def manage_person_tool(method=str, user_id=int, person_id=int, area_name=str,
                        method_name=str, tool_name=str, tool_type=str,
                        web_address=str, new_name=str,  proficiency=str, 
                        notes=str):
    
    input_list = [method, user_id, person_id, area_name, method_name, tool_name,
            tool_type, web_address, new_name, proficiency, notes, False, 
            None]
    
    connection = engine.raw_connection()
    try:
        cursor_obj = connection.cursor()
        cursor_obj.callproc("sp_ManagePersonTool", input_list)
        results = list(cursor_obj.fetchall())
        cursor_obj.close()
        connection.commit()
    finally:
        connection.close()

    return results
