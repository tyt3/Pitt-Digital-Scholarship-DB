# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, CHAR, \
    String, Table, text, Text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from .database import Base
from uuid import uuid4


# Set metadata
metadata = Base.metadata

"""Modes/Classes"""

class User(Base, UserMixin):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(16), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    user_password = Column(String(256), nullable=False)
    api_key = Column(String(50), nullable=False, unique=True)
    fk_permission_id = Column(Integer, nullable=False)
    account_created = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_login = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    can_add = False
    can_update = False
    can_delete = False

    def __init__(self, user_name, first_name, last_name, email, user_password, \
                 api_key, permission_level):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_password = user_password
        self.api_key = api_key
        self.fk_permission_id = permission_level

    def set_permissions(self, entity=None):
        if self.fk_permission_id > 1:
            self.can_add = True

        if entity:
            if self.fk_permission_id == 4:
                self.can_update = True
                self.can_delete = True
            elif self.fk_permission_id == 3:
                self.can_update = True
            elif entity.added_by == self.user_id:
                self.can_update = True
    
    def __rep__(self):
        return f"{self.user_name}"

    def get_id(self):
        return (self.user_id)
    

class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True, default=uuid4())
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    title = Column(String(100))
    pronouns = Column(String(50))
    email = Column(String(256), nullable=False, unique=True)
    web_address = Column(String(500))
    phone = Column(CHAR(10))
    scheduler_address = Column(String(50))
    other_contact = Column(String(500))
    preferred_contact = Column(String(50))
    support_type = Column(String(50), nullable=False)
    bio = Column(String(5000))
    notes = Column(String(5000))
    photo_url = Column(String(300))
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    user = relationship('User')
    fk_units = relationship('Unit', secondary='person_unit')

    def __init__(self, first_name=str, last_name=str, title=str, pronouns=str, 
                 email=str, web_address=str, phone=str, scheduler_address=str, 
                 other_contact=str, preferred_contact=str, support_type=str, 
                 bio=str, notes=str, photo_url=str, added_by=str):
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.pronouns = pronouns
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.scheduler_address = scheduler_address
        self.other_contact = other_contact
        self.preferred_contact = preferred_contact
        self.support_type = support_type
        self.bio = bio
        self.photo_url = photo_url
        self.notes = notes
        self.added_by = added_by

    def __rep__(self):
        return f"{self.first_name} {self.last_name}, {self.title}, {self.email}"
    
    def get_id(self):
        return (self.person_id)
    
    
class Unit(Base):
    __tablename__ = 'unit'

    unit_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True, default=uuid4())
    unit_name = Column(String(100), nullable=False, unique=True)
    unit_type = Column(String(50), nullable=False)
    email = Column(String(256), unique=True)
    phone = Column(CHAR(10))
    other_contact = Column(String(500))
    preferred_contact = Column(String(50))
    web_address = Column(String(500))
    description = Column(String(5000))
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    user = relationship('User')
    subunits = relationship(
        'Unit',
        secondary='unit_subunit',
        primaryjoin='Unit.unit_id == unit_subunit.c.fk_unit_id',
        secondaryjoin='Unit.unit_id == unit_subunit.c.subunit_id'
    )

    def __init__(self, unit_name, unit_type, email, web_address, phone, 
                 other_contact, preferred_contact, description, added_by):
        self.unit_name = unit_name
        self.unit_type = unit_type
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.other_contact = other_contact
        self.preferred_contact = preferred_contact
        self.description = description
        self.added_by = added_by

    def __rep__(self):
        return f"{self.unit_name} ({self.unit_type})"
    
    def get_id(self):
        return (self.unit_id)


class Funding(Base):
    __tablename__ = 'funding'

    funding_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True, default=uuid4())
    funding_name = Column(String(100), nullable=False, unique=True)
    funding_type = Column(String(50), nullable=False)
    payment_type = Column(String(50), nullable=False)
    payment_amount = Column(Float(asdecimal=True))
    career_level = Column(String(50), nullable=False)
    duration = Column(String(50))
    frequency = Column(String(50))
    web_address = Column(String(500))
    description = Column(String(5000))
    notes = Column(String(5000))
    campus = Column(String(50), nullable=False)
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    user = relationship('User')
    fk_units = relationship('Unit', secondary='unit_funding')

    def __init__(self, funding_name, funding_type, payment_type, payment_amount,
                 career_level, duration, frequency, web_address, notes, campus, 
                 added_by):
        self.funding_name = funding_name
        self.funding_type = funding_type
        self.payment_type = payment_type
        self.payment_amount = payment_amount
        self.career_level = career_level
        self.duration = duration
        self.frequency = frequency
        self.web_address = web_address
        self.notes = notes
        self.campus = campus
        self.added_by = added_by

    def __rep__(self):
        return f"{self.funding_name}, {self.funding_type}, {self.amount}, \
            {self.web_address}"
    
    def get_id(self):
        return (self.funding_id)


class Permission(Base):
    __tablename__ = 'permission'

    permission_id = Column(Integer, primary_key=True, unique=True)
    permission_code = Column(String(256))


class Affiliation(Base):
    __tablename__ = 'affiliation'

    affiliation_id = Column(Integer, primary_key=True)
    affiliation_type = Column(String(50), nullable=False)

    fk_persons = relationship('Person', secondary='person_affiliation')

    def __init__(self, affiliation_type):
        self.affiliation_type = affiliation_type

    def __rep__(self):
        return f"{self.affiliation_type}"


class Proficiency(Base):
    __tablename__ = 'proficiency'

    proficiency_id = Column(Integer, primary_key=True)
    proficiency_level = Column(String(50), nullable=False)


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    building_name = Column(String(100))
    room_number = Column(String(25))
    street_address = Column(String(200), nullable=False)
    address_2 = Column(String(200))
    city = Column(String(50), nullable=False)
    state = Column(CHAR(2), nullable=False)
    zipcode = Column(Integer, nullable=False)
    campus = Column(String(50), nullable=False)
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')
    fk_persons = relationship('Person', secondary='person_address')
    fk_units = relationship('Unit', secondary='unit_address')

    def __init__(self, building_name, room_number, street_address, 
                 address_2, city, state, zipcode, campus, added_by):
        self.building_name = building_name
        self.room_number = room_number
        self.street_address = street_address
        self.address_2 = address_2 
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.campus = campus
        self.added_by = added_by

    def __rep__(self):
        return f"{self.room_number}, {self.building_name}\n \
            {self.street_address}, {self.city}, {self.state}, {self.zipcode}"
    
    def __str__(self):
        fields = [f"{ self.room_number } { self.building_name}", self.street_address, 
        self.address_2, self.city, self.state, self.zipcode, self.campus]

        return ",".join(fields)

    def get_id(self):
        return (self.address_id)


class Area(Base):
    __tablename__ = 'area'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(100), nullable=False, unique=True)
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')
    fk_methods = relationship('Method', secondary='method_area')
    fk_resources = relationship('Resource', secondary='resource_area')
    fk_tools = relationship('Tool', secondary='tool_area')

    def __init__(self, area_name, added_by):
        self.area_name = area_name
        self.added_by = added_by

    def __rep__(self):
        return f"{self.area_name}"
    
    def get_id(self):
        return (self.area_id)
    

class Method(Base):
    __tablename__ = 'method'

    method_id = Column(Integer, primary_key=True)
    method_name = Column(String(100), nullable=False, unique=True)
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')
    fk_tools = relationship('Tool', secondary='method_tool')

    def __init__(self, method_name, added_by):
        self.method_name = method_name
        self.added_by = added_by

    def __rep__(self):
        return f"{self.method_name}"
    
    def get_id(self):
        return (self.method_id)


class Tool(Base):
    __tablename__ = 'tool'

    tool_id = Column(Integer, primary_key=True)
    tool_name = Column(String(100), nullable=False, unique=True)
    tool_type = Column(String(50))
    web_address = Column(String(300))
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')

    def __init__(self, tool_name, tool_type, web_address, added_by):
        self.tool_name = tool_name
        self.tool_type = tool_type
        self.web_address = web_address
        self.added_by = added_by

    def __rep__(self):
        return f"{self.tool_name}"
    
    def get_id(self):
        return (self.tool_id)
    

class Resource(Base):
    __tablename__ = 'resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(100), nullable=False, unique=True)
    resource_type = Column(String(50))
    web_address = Column(String(300))
    added_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')

    def __init__(self, resource_name, resource_type, web_addres, added_by):
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.web_address = web_addres
        self.added_by = added_by

    def __rep__(self):
        return f"{self.resource_name}"
    
    def get_id(self):
        return (self.resource_id)


class PersonArea(Base):
    __tablename__ = 'person_area'

    fk_person_id = Column(ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_area_id = Column(ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    fk_proficiency_id = Column(ForeignKey('proficiency.proficiency_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    notes = Column(String(5000))

    fk_area = relationship('Area')
    fk_person = relationship('Person')
    fk_proficiency = relationship('Proficiency')

    def __init__(self, fk_person_id, fk_area_id, fk_proficiency_id, notes):
        self.fk_person_id = fk_person_id
        self.fk_area_id = fk_area_id
        self.fk_proficiency_id = fk_proficiency_id
        self.notes = notes


class PersonMethod(Base):
    __tablename__ = 'person_method'

    fk_person_id = Column(ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_method_id = Column(ForeignKey('method.method_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    fk_proficiency_id = Column(ForeignKey('proficiency.proficiency_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    notes = Column(String(5000))

    fk_method = relationship('Method')
    fk_person = relationship('Person')
    fk_proficiency = relationship('Proficiency')

    def __init__(self, fk_person_id, fk_method_id, fk_proficiency_id, notes):
        self.fk_person_id = fk_person_id
        self.fk_method_id = fk_method_id
        self.fk_proficiency_id = fk_proficiency_id
        self.notes = notes

    def __rep__(self):
        return f"{self.fk_person_id}, {self.fk_method_id}"


class PersonTool(Base):
    __tablename__ = 'person_tool'

    fk_person_id = Column(ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_tool_id = Column(ForeignKey('tool.tool_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    fk_proficiency_id = Column(ForeignKey('proficiency.proficiency_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    notes = Column(String(5000))

    fk_person = relationship('Person')
    fk_proficiency = relationship('Proficiency')
    fk_tool = relationship('Tool')

    def __init__(self, fk_person_id, fk_tool_id, fk_proficiency_id, notes):
        self.fk_person_id = fk_person_id
        self.fk_tool_id = fk_tool_id
        self.fk_proficiency_id = fk_proficiency_id
        self.notes = notes


class UnitResource(Base):
    __tablename__ = 'unit_resource'

    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_resource_id = Column(ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    notes = Column(String(5000))

    fk_resource = relationship('Resource')
    fk_unit = relationship('Unit')


class Modification(Base):
    __tablename__ = 'modification'

    modification_id = Column(Integer, primary_key=True)
    modification = Column(String(500), nullable=False)
    modified_by = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    modification_date = Column(DateTime, nullable=False)

    user = relationship('User')

    def __init__(self, modification, modified_by, modification_date):
        self.modification = modification
        self.modified_by = modified_by
        self.modification_date = modification_date

    def __rep__(self):
        return f"{self.entity_id}, {self.modification}"
    
    def get_id(self):
        return (self.modification_id)


""" VIEWS """

t_vw_addresses = Table(
    'vw_addresses', metadata,
    Column('entity_id', Integer, server_default=text("'0'")),
    Column('public_id', String(36)),
    Column('entity_name', String(201)),
    Column('address_id', Integer, server_default=text("'0'")),
    Column('building_name', String(100)),
    Column('room_number', String(25)),
    Column('street_address', String(200)),
    Column('address_2', String(200)),
    Column('city', String(50)),
    Column('state', CHAR(2)),
    Column('zipcode', Integer, server_default=text("'0'")),
    Column('campus', String(50)),
    Column('added_by', Integer, server_default=text("'0'")),
    Column('date_added', DateTime, server_default=text("'0000-00-00 00:00:00'"))
)


t_vw_funding = Table(
    'vw_funding', metadata,
    Column('funding_public_id', String(36)),
    Column('funding_id', Integer, server_default=text("'0'")),
    Column('funding_name', String(100)),
    Column('funding_type', String(50)),
    Column('payment_type', String(50)),
    Column('payment_amount', Float(asdecimal=True)),
    Column('career_level', String(50)),
    Column('duration', String(50)),
    Column('frequency', String(50)),
    Column('web_address', String(500)),
    Column('unit_public_id', String(36)),
    Column('unit_name', String(100)),
    Column('campus', String(50)),
    Column('added_by', Integer),
    Column('last_modified', DateTime)
)


t_vw_person_support = Table(
    'vw_person_support', metadata,
    Column('person_id', Integer, server_default=text("'0'")),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('support_type', String(50)),
    Column('area_id', Integer, server_default=text("'0'")),
    Column('area_name', String(100)),
    Column('area_proficiency_id', Integer),
    Column('area_proficiency_level', String(50)),
    Column('area_notes', String(5000)),
    Column('method_id', Integer, server_default=text("'0'")),
    Column('method_name', String(100)),
    Column('method_proficiency_id', Integer, server_default=text("'0'")),
    Column('method_proficiency', String(50)),
    Column('method_notes', String(5000)),
    Column('tool_id', Integer, server_default=text("'0'")),
    Column('tool_name', String(100)),
    Column('tool_type', String(50)),
    Column('tool_website', String(300)),
    Column('tool_proficiency_id', Integer, server_default=text("'0'")),
    Column('tool_proficiency', String(50)),
    Column('tool_notes', String(5000)),
    Column('campus', String(50))
)


t_vw_person_units = Table(
    'vw_person_units', metadata,
    Column('person_public_id', String(36)),
    Column('person_name', String(201)),
    Column('person_email', String(256)),
    Column('support_type', String(50)),
    Column('photo_url', String(300)),
    Column('unit_id', Integer, server_default=text("'0'")),
    Column('unit_public_id', String(36)),
    Column('unit_name', String(100)),
    Column('parent_unit_public_id', String(36)),
    Column('parent_unit_name', String(100))
)


t_vw_unit_support = Table(
    'vw_unit_support', metadata,
    Column('fk_public_id', String(36)),
    Column('unit_name', String(100)),
    Column('area_id', Integer),
    Column('area_name', String(100)),
    Column('resource_id', Integer),
    Column('resource_name', String(100)),
    Column('resource_type', String(50)),
    Column('resource_website', String(300)),
    Column('resource_notes', Text)
)


t_vw_units = Table(
    'vw_units', metadata,
    Column('public_id', String(36)),
    Column('unit_name', String(100)),
    Column('unit_type', String(50)),
    Column('email', String(256)),
    Column('phone', CHAR(10)),
    Column('other_contact', String(500)),
    Column('preferred_contact', String(50)),
    Column('web_address', String(500)),
    Column('description', String(5000)),
    Column('parent_unit_id', Integer, server_default=text("'0'")),
    Column('parent_unit_public_id', String(36)),
    Column('parent_unit_name', String(100)),
    Column('campus', String(50)),
    Column('added_by', Integer),
    Column('date_added', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('last_modified', DateTime)
)


""" Junction Tables """

t_method_area = Table(
    'method_area', metadata,
    Column('fk_method_id', ForeignKey('method.method_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_method_tool = Table(
    'method_tool', metadata,
    Column('fk_method_id', ForeignKey('method.method_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_tool_id', ForeignKey('tool.tool_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_person_address = Table(
    'person_address', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_address_id', ForeignKey('address.address_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_person_affiliation = Table(
    'person_affiliation', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_affiliation_id', ForeignKey('affiliation.affiliation_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_person_support = Table(
    'person_support', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('fk_method_id', ForeignKey('method.method_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('fk_tool_id', ForeignKey('tool.tool_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('date_added', DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)


t_person_unit = Table(
    'person_unit', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_resource_area = Table(
    'resource_area', metadata,
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_tool_area = Table(
    'tool_area', metadata,
    Column('fk_tool_id', ForeignKey('tool.tool_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_unit_address = Table(
    'unit_address', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_address_id', ForeignKey('address.address_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)

t_unit_subunit = Table(
    'unit_subunit', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('subunit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)

t_unit_funding = Table(
    'unit_funding', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_funding_id', ForeignKey('funding.funding_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)

t_unit_support = Table(
    'unit_support', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    Column('date_added', DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)
