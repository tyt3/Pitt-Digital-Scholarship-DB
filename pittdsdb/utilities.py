from flask_login import current_user
from .database import db_session, engine
from .models import *


""" Modifcation Function """

def log_modification(description, timestamp):
    modification = Modification(modification=description,
                                modified_by=current_user.user_id,
                                modification_date=timestamp)
    
    # Add modification log to database
    db_session.add(modification)
    db_session.commit()


def check_relation(table, entity_1_type, entity_1_id, entity_2_type, entity_2_id):
    prefix = ""
    if table != "vw_person_support":
        prefix = "fk_"

    query = f"SELECT * FROM { table } \
            WHERE { prefix }{entity_1_type}_id = {entity_1_id} \
            AND { prefix }{entity_2_type}_id = {entity_2_id};"
    results = db_session.execute(text(query)).first()

    if results:
        return True
    return False

