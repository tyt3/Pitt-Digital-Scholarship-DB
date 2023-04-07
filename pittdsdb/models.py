# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, \
    SmallInteger, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base


# Set metadata
metadata = Base.metadata

"""Model Classes"""

class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    building_name = Column(String(50))
    room_number = Column(String(50))
    address_1 = Column(String(50), nullable=False)
    address_2 = Column(String(50))
    address_3 = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zipcode = Column(Integer, nullable=False)
    campus = Column(String(50), nullable=False)

    fk_departments = relationship('Department', secondary='department_address')
    fk_persons = relationship('Person', secondary='person_address')
    fk_subunits = relationship('Subunit', secondary='subunit_address')
    fk_units = relationship('Unit', secondary='unit_address')

    def __init__(self, address_id, building_name, room_number, address_1, 
                 address_2, address_3, city, state, zipcode, campus):
        self.address = address_id
        self.building_name = building_name
        self.room_number = room_number
        self.address_1 = address_1
        self.address_2 = address_2 
        self.address_3 = address_3
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.campus = campus


class Affiliation(Base):
    __tablename__ = 'affiliation'

    affiliation_id = Column(Integer, primary_key=True)
    affiliation_type = Column(String(50), nullable=False)

    fk_persons = relationship('Person', secondary='person_affiliation')


class Area(Base):
    __tablename__ = 'area'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(50), nullable=False)

    fk_methods = relationship('Method', secondary='method_area')
    fk_persons = relationship('Person', secondary='person_area')
    fk_resources = relationship('Resource', secondary='resource_area')
    fk_tools = relationship('Tool', secondary='tool_area')


class Funding(Base):
    __tablename__ = 'funding'

    funding_id = Column(Integer, primary_key=True)
    funding_name = Column(String(50), nullable=False)
    funding_type = Column(String(50), nullable=False)
    payment_type = Column(String(50), nullable=False)
    amount = Column(Float(asdecimal=True))
    career_level = Column(String(50), nullable=False)
    duration = Column(String(50))
    frequency = Column(String(50))
    web_address = Column(String(50))
    last_modified = Column(DateTime, nullable=False)

    fk_subunits = relationship('Subunit', secondary='subunit_funding')
    fk_units = relationship('Unit', secondary='unit_funding')


class Method(Base):
    __tablename__ = 'method'

    method_id = Column(Integer, primary_key=True)
    method_name = Column(String(50), nullable=False)

    fk_tools = relationship('Tool', secondary='method_tool')

    def __init__(self, method_name):
        self.method_name = method_name


class Proficiency(Base):
    __tablename__ = 'proficiency'

    proficiency_id = Column(Integer, primary_key=True)
    proficiency_level = Column(String(50), nullable=False)


class Resource(Base):
    __tablename__ = 'resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(50), nullable=False)

    fk_subunits = relationship('Subunit', secondary='subunit_resource')
    fk_units = relationship('Unit', secondary='unit_resource')


class Tool(Base):
    __tablename__ = 'tool'

    tool_id = Column(Integer, primary_key=True)
    tool_name = Column(String(50), nullable=False)
    web_address = Column(String(50))
    github = Column(String(50))


class Unit(Base):
    __tablename__ = 'unit'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(String(50), nullable=False)
    unit_type = Column(String(50), nullable=False)
    email = Column(String(50))
    web_address = Column(String(50))
    preferred_contact = Column(String(50))
    descrption = Column(String(500))


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    user_password = Column(String(15), nullable=False)
    api_key = Column(String(50), nullable=False)
    permission_level = Column(Integer, nullable=False)
    account_created = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=False)


class Department(Base):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(50), nullable=False)
    email = Column(String(50))
    web_address = Column(String(50))
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    descrption = Column(String(500))
    last_modified = Column(DateTime, nullable=False)

    fk_unit = relationship('Unit')
    fk_fundings = relationship('Funding', secondary='department_funding')
    fk_resources = relationship('Resource', secondary='department_resource')
    fk_persons = relationship('Person', secondary='person_department')


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


class Modification(Base):
    __tablename__ = 'modification'

    modification_id = Column(Integer, primary_key=True)
    entity_type = Column(String(10), nullable=False)
    entity_id = Column(Integer, nullable=False)
    modification = Column(String(500), nullable=False)
    modified_by = Column(ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    modificaiton_date = Column(DateTime, nullable=False)

    user = relationship('User')


class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    title = Column(String(50))
    pronouns = Column(String(50))
    email = Column(String(50), nullable=False)
    web_address = Column(String(50))
    phone = Column(Integer)
    scheduler_address = Column(String(50))
    preferred_contact = Column(String(50))
    support_type = Column(String(50), nullable=False)
    bio = Column(String(500), nullable=False)
    added_by = Column(ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    notes = Column(String(8000))

    user = relationship('User')
    fk_subunits = relationship('Subunit', secondary='person_subunit')
    fk_units = relationship('Unit', secondary='person_unit')

    def __init__(self, person_id, first_name, last_name, title, pronouns, email,
                 web_address, phone, scheduler_address, preferred_contact, 
                 support_type, bio, added_by, date_added, last_modified, notes):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.pronouns = pronouns
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.scheduler_address = scheduler_address
        self.preferred_contact = preferred_contact
        self.support_type = support_type
        self.bio = bio
        self.added_by = added_by
        self.date_added = date_added
        self.last_modified = last_modified
        self.notes = notes


t_resource_area = Table(
    'resource_area', metadata,
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Subunit(Base):
    __tablename__ = 'subunit'

    subunit_id = Column(Integer, primary_key=True)
    subunit_name = Column(String(50), nullable=False)
    subunit_type = Column(String(50), nullable=False)
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    descrption = Column(String(500))
    last_modified = Column(DateTime, nullable=False)

    fk_unit = relationship('Unit')
    fk_units = relationship('Unit', secondary='unit_subunit')


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


t_unit_funding = Table(
    'unit_funding', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_funding_id', ForeignKey('funding.funding_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_unit_resource = Table(
    'unit_resource', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_department_address = Table(
    'department_address', metadata,
    Column('fk_department_id', ForeignKey('department.department_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_address_id', ForeignKey('address.address_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_department_funding = Table(
    'department_funding', metadata,
    Column('fk_department_id', ForeignKey('department.department_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_funding_id', ForeignKey('funding.funding_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_department_resource = Table(
    'department_resource', metadata,
    Column('fk_department_id', ForeignKey('department.department_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class DepartmentSubunit(Base):
    __tablename__ = 'department_subunit'

    fk_department_id = Column(ForeignKey('department.department_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_subunit_id = Column(ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    superior = Column(String(10), nullable=False)

    fk_department = relationship('Department')
    fk_subunit = relationship('Subunit')


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


t_person_area = Table(
    'person_area', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_person_department = Table(
    'person_department', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_department_id', ForeignKey('department.department_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class PersonMethod(Base):
    __tablename__ = 'person_method'

    fk_person_id = Column(ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_method_id = Column(ForeignKey('method.method_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    fk_proficiency_id = Column(ForeignKey('proficiency.proficiency_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    fk_method = relationship('Method')
    fk_person = relationship('Person')
    fk_proficiency = relationship('Proficiency')


t_person_subunit = Table(
    'person_subunit', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_subunit_id', ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class PersonTool(Base):
    __tablename__ = 'person_tool'

    fk_person_id = Column(ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    fk_tool_id = Column(ForeignKey('tool.tool_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    fk_proficiency_id = Column(ForeignKey('proficiency.proficiency_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    fk_person = relationship('Person')
    fk_proficiency = relationship('Proficiency')
    fk_tool = relationship('Tool')


t_person_unit = Table(
    'person_unit', metadata,
    Column('fk_person_id', ForeignKey('person.person_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_subunit_address = Table(
    'subunit_address', metadata,
    Column('fk_subunit_id', ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_address_id', ForeignKey('address.address_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_subunit_funding = Table(
    'subunit_funding', metadata,
    Column('fk_subunit_id', ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_funding_id', ForeignKey('funding.funding_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_subunit_resource = Table(
    'subunit_resource', metadata,
    Column('fk_subunit_id', ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_unit_subunit = Table(
    'unit_subunit', metadata,
    Column('fk_unit_id', ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_subunit_id', ForeignKey('subunit.subunit_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)
