# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, CHAR, \
    String, Table, text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
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
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_departments = relationship('Department', secondary='department_address')
    fk_persons = relationship('Person', secondary='person_address')
    fk_subunits = relationship('Subunit', secondary='subunit_address')
    fk_units = relationship('Unit', secondary='unit_address')

    def __init__(self, building_name, room_number, address_1, 
                 address_2, address_3, city, state, zipcode, campus):
        self.building_name = building_name
        self.room_number = room_number
        self.address_1 = address_1
        self.address_2 = address_2 
        self.address_3 = address_3
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.campus = campus

    def __rep__(self):
        return f"{self.room_number}, {self.building_name}, {self.campus}, \
    {self.address_1}, {self.city}, \
    {self.state}, {self.zipcode}"

    def get_id(self):
        return (self.address_id)


class Affiliation(Base):
    __tablename__ = 'affiliation'

    affiliation_id = Column(Integer, primary_key=True)
    affiliation_type = Column(String(50), nullable=False)

    fk_persons = relationship('Person', secondary='person_affiliation')

    def __init__(self, affiliation_type):
        self.affiliation_type = affiliation_type

    def __rep__(self):
        return f"{self.affiliation_type}"


class Area(Base):
    __tablename__ = 'area'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(50), nullable=False)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_methods = relationship('Method', secondary='method_area')
    fk_persons = relationship('Person', secondary='person_area')
    fk_resources = relationship('Resource', secondary='resource_area')
    fk_tools = relationship('Tool', secondary='tool_area')

    def __init__(self, area_name):
        self.area_name = area_name

    def __rep__(self):
        return f"{self.area_name}"
    
    def get_id(self):
        return (self.area_id)


class Funding(Base):
    __tablename__ = 'funding'

    funding_id = Column(Integer, primary_key=True)
    funding_name = Column(String(100), nullable=False)
    funding_type = Column(String(50), nullable=False)
    payment_type = Column(String(50), nullable=False)
    payment_amount = Column(Float(asdecimal=True))
    payment_frequency = Column(String(50), nullable=False)
    career_level = Column(String(50), nullable=False)
    duration = Column(String(50))
    frequency = Column(String(50))
    web_address = Column(String(50))
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_subunits = relationship('Subunit', secondary='subunit_funding')
    fk_units = relationship('Unit', secondary='unit_funding')

    def __init__(self, funding_name, funding_type, payment_type, payment_amount, \
                 payment_frequency, career_level, duration, frequency, \
                    web_address):
        self.funding_name = funding_name
        self.funding_type = funding_type
        self.payment_type = payment_type
        self.payment_amount = payment_amount
        self.payment_frequency = payment_frequency
        self.career_level = career_level
        self.duration = duration
        self.frequency = frequency
        self.web_address = web_address

    def __rep__(self):
        return f"{self.funding_name}, {self.funding_type}, {self.amount}, \
            {self.duration}, {self.frequency}, {self.web_address}"
    
    def get_id(self):
        return (self.funding_id)


class Method(Base):
    __tablename__ = 'method'

    method_id = Column(Integer, primary_key=True)
    method_name = Column(String(50), nullable=False)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_tools = relationship('Tool', secondary='method_tool')

    def __init__(self, method_name):
        self.method_name = method_name

    def __rep__(self):
        return f"{self.method_name}"
    
    def get_id(self):
        return (self.method_id)


class Permission(Base):
    __tablename__ = 'permission'

    permission_id = Column(Integer, primary_key=True, unique=True)
    permission_code = Column(String(256))


class Proficiency(Base):
    __tablename__ = 'proficiency'

    proficiency_id = Column(Integer, primary_key=True)
    proficiency_level = Column(String(50), nullable=False)


class Resource(Base):
    __tablename__ = 'resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(50), nullable=False, unique=True)
    resource_type = Column(String(50), nullable=False)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_subunits = relationship('Subunit', secondary='subunit_resource')
    fk_units = relationship('Unit', secondary='unit_resource')

    def __init__(self, resource_name, resource_type):
        self.resource_name = resource_name
        self.resource_type = resource_type

    def __rep__(self):
        return f"{self.resource_name}"
    
    def get_id(self):
        return (self.resource_id)


class Tool(Base):
    __tablename__ = 'tool'

    tool_id = Column(Integer, primary_key=True)
    tool_name = Column(String(50), nullable=False)
    web_address = Column(String(100))
    github = Column(String(100))
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    def __init__(self, tool_name, web_address, github):
        self.tool_name = tool_name
        self.web_address = web_address
        self.github = github

    def __rep__(self):
        return f"{self.tool_name}, {self.web_address}, {self.github}"
    
    def get_id(self):
        return (self.tool_id)


class Unit(Base):
    __tablename__ = 'unit'

    unit_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True)
    unit_name = Column(String(100), nullable=False)
    unit_type = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    web_address = Column(String(50))
    phone = Column(CHAR(10))
    preferred_contact = Column(String(50))
    description = Column(String(500))
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    def __init__(self, unit_name, unit_type, email, web_address, phone, preferred_contact, description):
        self.unit_name = unit_name
        self.unit_type = unit_type
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.preferred_contact = preferred_contact
        self.description = description

    def __rep__(self):
        return f"{self.unit_name} ({self.unit_type}), {self.email}, \
            {self.web_address}, {self.phone}, {self.preferred_contact}, \
                {self.description}"
    
    def get_id(self):
        return (self.unit_id)

class User(Base, UserMixin):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    user_password = Column(String(256), nullable=False)
    api_key = Column(String(50), nullable=False)
    permission_level = Column(Integer, nullable=False)
    account_created = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_login = Column(DateTime, nullable=False)
    can_add = False
    can_update_created = False
    can_update_all = False
    can_delete = False

    def __init__(self, user_name, first_name, last_name, email, user_password, \
                 api_key, permission_level, last_login):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_password = user_password
        self.api_key = api_key
        self.permission_level = permission_level
        self.last_login = last_login

    def set_permissions(self):
        if self.permission_level == 4:
            self.can_add = True
            self.can_update_created = True
            self.can_update_all = True
            self.can_delete= True
        elif self.permission_level == 3:
            self.can_add = True
            self.can_update_all = True
            self.can_update_created = True
        elif self.permission_level == 2:
            self.can_add = True
            self.can_update_created = True

    def get_id(self):
        return (self.user_id)
    
    
    def __rep__(self):
        return f"{self.user_name}"


t_vw_addresses = Table(
    'vw_addresses', metadata,
    Column('public_id', String(36)),
    Column('building_name', String(50)),
    Column('room_number', String(50)),
    Column('address_1', String(50)),
    Column('address_2', String(50)),
    Column('address_3', String(50)),
    Column('city', String(50)),
    Column('state', String(50)),
    Column('zipcode', Integer, server_default=text("'0'")),
    Column('campus', String(50))
)


t_vw_funding = Table(
    'vw_funding', metadata,
    Column('public_id', String(36)),
    Column('funding_id', Integer, server_default=text("'0'")),
    Column('funding_name', String(50)),
    Column('funding_type', String(50)),
    Column('payment_type', String(50)),
    Column('amount', Float(asdecimal=True)),
    Column('career_level', String(50)),
    Column('duration', String(50)),
    Column('frequency', String(50)),
    Column('web_address', String(50)),
    Column('campus', String(50)),
    Column('last_modified', DateTime, server_default=text("'0000-00-00 00:00:00'"))
)


t_vw_person_support = Table(
    'vw_person_support', metadata,
    Column('person_id', Integer, server_default=text("'0'")),
    Column('first_name', String(50)),
    Column('last_name', String(50)),
    Column('support_type', String(50)),
    Column('area_id', Integer, server_default=text("'0'")),
    Column('area_name', String(50)),
    Column('method_id', Integer, server_default=text("'0'")),
    Column('method_name', String(50)),
    Column('method_proficiency_id', Integer, server_default=text("'0'")),
    Column('method_proficiency', String(50)),
    Column('tool_id', Integer, server_default=text("'0'")),
    Column('tool_name', String(50)),
    Column('tool_proficiency_id', Integer, server_default=text("'0'")),
    Column('tool_proficiency', String(50)),
    Column('campus', String(50))
)


t_vw_unit_support = Table(
    'vw_unit_support', metadata,
    Column('public_id', String(36)),
    Column('entity_name', String(100)),
    Column('area_id', Integer),
    Column('area_name', String(50)),
    Column('resource_id', Integer, server_default=text("'0'")),
    Column('resource_name', String(50)),
    Column('campus', String(50))
)


class Department(Base):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True)
    department_name = Column(String(100), nullable=False)
    department_type = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    web_address = Column(String(50))
    phone = Column(CHAR(10))
    preferred_contact = Column(String(50))
    description = Column(String(500))
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_unit = relationship('Unit')
    fk_fundings = relationship('Funding', secondary='department_funding')
    fk_resources = relationship('Resource', secondary='department_resource')
    fk_persons = relationship('Person', secondary='person_department')

    def __init__(self, department_name, email, web_address, \
                 phone, fk_unit_id, description):
        self.department_name = department_name
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.fk_unit_id = fk_unit_id
        self.description = description

    def __rep__(self):
        return f"{self.department_name}, {self.email}, {self.web_address}, \
            {self.phone}, {self.description}"
    
    def get_id(self):
        return (self.department_id)


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

    def __init__(self, entity_type, entity_id, modification, modified_by, modificaiton_date):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.modification = modification
        self.modified_by = modified_by
        self.modificaiton_date = modificaiton_date

    def __rep__(self):
        return f"{self.modification}"
    
    def get_id(self):
        return (self.modification_id)


class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    title = Column(String(50))
    pronouns = Column(String(50))
    email = Column(String(100), nullable=False, unique=True)
    web_address = Column(String(50))
    phone = Column(CHAR(10))
    scheduler_address = Column(String(50))
    preferred_contact = Column(String(50))
    support_type = Column(String(50), nullable=False)
    bio = Column(String(500), nullable=False)
    added_by = Column(ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    notes = Column(String(8000))

    user = relationship('User')
    fk_subunits = relationship('Subunit', secondary='person_subunit')
    fk_units = relationship('Unit', secondary='person_unit')

    def __init__(self, first_name, last_name, title, pronouns, email,
                 web_address, phone, scheduler_address, preferred_contact, 
                 support_type, bio, added_by, notes):
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
        self.notes = notes
    
    def __rep__(self):
        return f"{self.first_name} {self.last_name}, {self.title}, {self.email}"
    
    def get_id(self):
        return (self.person_id)
    

t_resource_area = Table(
    'resource_area', metadata,
    Column('fk_resource_id', ForeignKey('resource.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('fk_area_id', ForeignKey('area.area_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Subunit(Base):
    __tablename__ = 'subunit'

    subunit_id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True)
    subunit_name = Column(String(100), nullable=False)
    subunit_type = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    web_address = Column(String(100))
    phone = Column(CHAR(10))
    preferred_contact = Column(String(50))
    description = Column(String(500))
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_added = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    last_modified = Column(DateTime, nullable=False, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    fk_unit = relationship('Unit')
    fk_units = relationship('Unit', secondary='unit_subunit')

    def __init__(self, subunit_name, subunit_type, email, web_address, phone, \
                 preferred_contact, description, fk_unit_id):
        self.subunit_name = subunit_name
        self.subunit_type = subunit_type
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.preferred_contact = preferred_contact
        self.description = description
        self.fk_unit_id = fk_unit_id

    def __rep__(self):
        return f"{self.subunit_name} ({self.subunit_type}), {self.email}, \
            {self.web_address}, {self.phone}, {self.preferred_contact}, \
                {self.description}"
    
    def get_id(self):
        return (self.subunit_id)


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

    def __init__(self, fk_department_id, fk_subunit_id, superior):
        self.fk_department_id = fk_department_id
        self.fk_subunit_id = fk_subunit_id
        self.superior = superior

    def __rep__(self):
        return f"{self.superior}"


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