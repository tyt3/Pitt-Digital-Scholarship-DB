from sqlalchemy.sql import text
from database import db_session
from models import *
from schemas import *

# m = Method.query.filter_by(method_id=5).first()
# db_session.add(m)
# #db_session.delete(m)
# db_session.commit()

def search_person(first_name, last_name, title, support_type, campus):
    sql = f'SELECT person_id FROM vw_person_support WHERE '
    empty = True

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
        sql += f'title LIKE "{title}"'
        empty = False
    if support_type:
        support_type_str = str(support_type).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'support_type IN "{support_type_str}"'
        empty = False
    if campus:
        campus = str(campus).replace('[', '(').replace(']', ')')
        if not empty:
            sql += f' AND '
        sql += f'support_type IN "{support_type}"'
        empty = False
    
    if empty:
        return "Please enter at least one parameter for your query from \
            id, first_name, last_name, support_type, campus"
    else:
        result = db_session.execute(text(sql + ';')).fetchall()
        result = list(set(list(zip(*result))[0]))

    person_list = Person.query.filter(Person.person_id.in_(result))

    for person in person_list:
        print(person.first_name)

    #return print(person_list)

    #return print(result)


if __name__ == '__main__':
    search_person(first_name="Tyrica",
                  last_name="",
                  title="",
                  support_type="",
                  campus="")

