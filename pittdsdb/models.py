# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, \
    String, Table
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

    def __rep__(self):
        return f"{self.room_number}, {self.building_name}, {self.campus}, {self.address_1}, {self.address_2}, {self.address_3}, {self.city}, {self.state} - {self.zipcode}"




class Affiliation(Base):
    __tablename__ = 'affiliation'

    affiliation_id = Column(Integer, primary_key=True)
    affiliation_type = Column(String(50), nullable=False)

    fk_persons = relationship('Person', secondary='person_affiliation')

    def __init__(self, affiliation_id, affiliation_type):
        self.affiliation_id = affiliation_id
        self.affiliation_type = affiliation_type

    def __rep__(self):
        return f"{self.affiliation_type}"


class Area(Base):
    __tablename__ = 'area'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(50), nullable=False)

    fk_methods = relationship('Method', secondary='method_area')
    fk_persons = relationship('Person', secondary='person_area')
    fk_resources = relationship('Resource', secondary='resource_area')
    fk_tools = relationship('Tool', secondary='tool_area')

    def __init__(self, area_id, area_name):
        self.area_id = area_id
        self.area_name = area_name

    def __rep__(self):
        return f"{self.area_name}"


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
    web_address = Column(String(100))
    last_modified = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    fk_subunits = relationship('Subunit', secondary='subunit_funding')
    fk_units = relationship('Unit', secondary='unit_funding')

    def __init__(self, funding_id, funding_name, funding_type, payment_type, amount, career_level, duration, frequency, web_address, last_modified):
        self.funding_id = funding_id
        self.funding_name = funding_name
        self.funding_type = funding_type
        self.payment_type = payment_type
        self.amount = amount
        self.career_level = career_level
        self.duration = duration
        self.frequency = frequency
        self.web_address = web_address
        self.last_modified = last_modified

    def __rep__(self):
        return f"{self.funding_name}, {self.funding_type}, {self.amount}, {self.duration}, {self.frequency}, {self.web_address}"



class Method(Base):
    __tablename__ = 'method'

    method_id = Column(Integer, primary_key=True)
    method_name = Column(String(50), nullable=False)

    fk_tools = relationship('Tool', secondary='method_tool')

    def __init__(self, method_id, method_name):
        self.method_id = method_id
        self.method_name = method_name

    def __rep__(self):
        return f"{self.method_name}"
    

class Permission(Base):
    __tablename__ = 'permission'

    permission_id = Column(Integer, primary_key=True, unique=True)
    permission_code = Column(String(256))

    def __init__(self, permission_id, permission_code):
        self.permission_id = permission_id
        self.permission_code = permission_code

    def __rep__(self):
        return f"{self.permission_code}"
    

class Proficiency(Base):
    __tablename__ = 'proficiency'

    proficiency_id = Column(Integer, primary_key=True)
    proficiency_level = Column(String(50), nullable=False)

    def __init__(self, proficiency_id, proficiency_level):
        self.proficiency_id = proficiency_id
        self.proficiency_level = proficiency_level

    def __rep__(self):
        return f"{self.proficiency_level}"


class Resource(Base):
    __tablename__ = 'resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(50), nullable=False)

    fk_subunits = relationship('Subunit', secondary='subunit_resource')
    fk_units = relationship('Unit', secondary='unit_resource')

    def __init__(self, resource_id, resource_name):
        self.resource_id = resource_id
        self.resource_name = resource_name

    def __rep__(self):
        return f"{self.resource_name}"


class Tool(Base):
    __tablename__ = 'tool'

    tool_id = Column(Integer, primary_key=True)
    tool_name = Column(String(50), nullable=False)
    web_address = Column(String(100))
    github = Column(String(50))

    def __init__(self, tool_id, tool_name, web_address, github):
        self.tool_id = tool_id
        self.tool_name = tool_name
        self.web_address = web_address
        self.github = github

    def __rep__(self):
        return f"{self.tool_name}, {self.web_address}, {self.github}"


class Unit(Base):
    __tablename__ = 'unit'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(String(50), nullable=False)
    unit_type = Column(String(50), nullable=False)
    email = Column(String(50))
    web_address = Column(String(100))
    phone = Column(String(10))
    preferred_contact = Column(String(50))
    description = Column(String(500))
    last_modified = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    def __init__(self, unit_id, unit_name, unit_type, email, web_address, phone, preferred_contact, description, last_modified):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.unit_type = unit_type
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.preferred_contact = preferred_contact
        self.description = description
        self.last_modified = last_modified

    def __rep__(self):
        return f"{self.unit_name} ({self.unit_type}), {self.email}, {self.web_address}, {self.phone}, {self.preferred_contact}, {self.description}"


class User(Base, UserMixin):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    user_password = Column(String(15), nullable=False)
    api_key = Column(String(50), nullable=False)
    permission_level = Column(Integer, nullable=False)
    account_created = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)
    last_login = Column(DateTime, nullable=False)
    can_add = False
    can_update_created = False
    can_update_all = False
    can_delete= False

    def __init__(self, user_id, user_name, first_name, last_name, email, user_password, api_key, permission_level, account_created, last_login):
        self.user_id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_password = user_password
        self.api_key = api_key
        self.permission_level = permission_level
        self.account_created = account_created

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


class Department(Base):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(50), nullable=False)
    email = Column(String(50))
    web_address = Column(String(100))
    phone = Column(String(10))
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    description = Column(String(500))
    last_modified = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    fk_unit = relationship('Unit')
    fk_fundings = relationship('Funding', secondary='department_funding')
    fk_resources = relationship('Resource', secondary='department_resource')
    fk_persons = relationship('Person', secondary='person_department')

    def __init__(self, department_id, department_name, email, web_address, phone, fk_unit_id, description, last_modified):
        self.department_id = department_id
        self.department_name = department_name
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.fk_unit_id = fk_unit_id
        self.description = description
        self.last_modified = last_modified

    def __rep__(self):
        return f"{self.department_name}, {self.email}, {self.web_address}, {self.phone}, {self.description}"



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
    modificaiton_date = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    user = relationship('User')

    def __init__(self, modification_id, entity_type, entity_id, modification, modified_by, modificaiton_date):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.modification = modification
        self.modified_by = modified_by

    def __rep__(self):
        return f"{self.modification}"


class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    title = Column(String(50))
    pronouns = Column(String(50))
    email = Column(String(50), nullable=False)
    web_address = Column(String(100))
    phone = Column(String(10))
    scheduler_address = Column(String(50))
    preferred_contact = Column(String(50))
    support_type = Column(String(50), nullable=False)
    bio = Column(String(500), nullable=False)
    added_by = Column(ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_added = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)
    last_modified = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)
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
    
    def __rep__(self):
        return f"{self.first_name} {self.last_name}, {self.title}, {self.email}"


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
    email = Column(String(50), nullable=False)
    web_address = Column(String(100))
    phone = Column(String(10))
    preferred_contact = Column(String(50))
    description = Column(String(500))
    fk_unit_id = Column(ForeignKey('unit.unit_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    last_modified = Column(DateTime, default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    fk_unit = relationship('Unit')
    fk_units = relationship('Unit', secondary='unit_subunit')

    def __init__(self, subunit_id, subunit_name, subunit_type, email, web_address, phone, preferred_contact, description, last_modified):
        self.subunit_id = subunit_id
        self.subunit_name = subunit_name
        self.subunit_type = subunit_type
        self.email = email
        self.web_address = web_address
        self.phone = phone
        self.preferred_contact = preferred_contact
        self.description = description
        self.fk_unit_id = fk_unit_id
        self.last_modified = last_modified

    def __rep__(self):
        return f"{self.subunit_name} ({self.subunit_type}), {self.email}, {self.web_address}, {self.phone}, {self.preferred_contact}, {self.description}"


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

    def __init__(self, fk_person_id, fk_method_id, fk_proficiency_id):
        self.fk_person_id = fk_person_id
        self.fk_method_id = fk_method_id
        self.fk_proficiency_id = fk_proficiency_id


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

    def __init__(self, fk_person_id, fk_tool_id, fk_proficiency_id):
        self.fk_person_id = fk_person_id
        self.fk_tool_id = fk_tool_id
        self.fk_proficiency_id = fk_proficiency_id


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
