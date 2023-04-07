from database import db_session
from models import Method

m = Method.query.filter_by(method_id=5).first()
db_session.add(m)
#db_session.delete(m)
db_session.commit()
