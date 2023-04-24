from .database import db_session
from .models import *

vocab = {
    'affiliation_type': [
        'Doctoral',
        'Faculty',
        'Masters',
        'Partner - Community',
        'Partner - Other University',
        'Postdoctoral',
        'Staff',
        'Undergraduate',
        'Other'
        ],
    'campus': [
        'Bradford',
        'Greensburg',
        'Johnstown',
        'Pittsburgh',
        'Titusville'
        ],
    'career_level': [
        'Undergraduate',
        'Masters',
        'Doctoral',
        'Postdoctoral',
        'Professional'
        ],
    'entity_type': [
        'person',
        'unit',
        'department',
        'subunit'
        ],
    'frequency': [
        'Annual',
        'Biannual',
        'Semester',
        'Fall',
        'Spring',
        'Summer',
        'Other'
        ],
    'funding_type': [
        'Fellowship',
        'Graduate Student Assistant',
        'Grant',
        'Internship',
        'Research Assistant',
        'Scholarship',
        'Other'
        ],
    'payment_type': [
        'Hourly',
        'Stipend',
        'Other'
        ],
    'preferred_contact': [
        'Email',
        'Phone',
        'Appointment Scheduler',
        'Other Contact Method'
        ],
    'proficiency_level': [
        'Fundamental Awareness (basic knowledge)',
        'Novice (limited experience)',
        'Intermediate (practical application)',
        'Advanced (applied theory)',
        'Expert (recognized authority)'
        ],
    'support_type': [
        'Collaboratory only',
        'Formal',
        'Informal'
        ],
    'unit_type': [
        'Center',
        'Collaborative',
        'Department',
        'Group',
        'Lab',
        'Library',
        'Museum',
        'Office',
        'School',
        'Team',
        'Unit',
        'Other'
        ],
    'tool_type': [
        'Command-line Application',
        'Desktop Application',
        'Programming Language',
        'Mobile Application',
        'Web Application',
        'Web Browser Plugin',
        'Other'
    ],
}

# Get entity values
area = None
try:
    areas = list(zip(*db_session.query(Area.area_name).distinct()))[0]
except:
    pass

campuses = None
try:
    campuses = list(zip(*db_session.query(Address.campus).distinct()))[0]
except:
    pass

career_levels = None
try:
    career_levels = list(zip(*db_session.query(Funding.career_level).distinct()))[0]
except:
    pass

funding_types = None
try:
    funding_types = list(zip(*db_session.query(Funding.funding_type).distinct()))[0]
except:
    pass

payment_types = None
try:
    payment_types = list(zip(*db_session.query(Funding.payment_type).distinct()))[0]
except:
    pass

methods = None
try:
    methods = list(zip(*db_session.query(Method.method_name).distinct()))[0]
except:
    pass

resources = None
try:
    resources = list(zip(*db_session.query(Resource.resource_type).distinct()))[0]
except:
    pass

support_types = None
try:
    support_types = list(zip(*db_session.query(Person.support_type).distinct()))[0]
except:
    pass

tools = None
try:
    tools = list(zip(*db_session.query(Tool.tool_name).distinct()))[0]
except:
    pass

units = None
try:
    units = list(zip(*db_session.query(Unit.unit_name).distinct()))[0]
except:
    pass

subunits = None
try:
    subunits = list(zip(*db_session.query(Subunit.subunit_name).distinct()))[0]
except:
    pass

entities = [areas, campuses, career_levels, funding_types, payment_types, 
            methods, resources, support_types, tools, units, subunits]

existing = {
    'areas': None,
    'campuses': None,
    'career_levels': None,
    'funding_types': None,
    'payment_types': None,
    'methods': None,
    'resources': None,
    'support_types': None,
    'tools': None,
    'units': None,
    'subunits': None
}

i = 0
for entity in existing:
    existing[entity] = entities[i]
    i += 1

area_name = ['2D Scanning and Digitization',
                 '3D Scanning and Modeling',
                 'Coding and Computation',
                 'Data',
                 'Digital Creation',
                 'Digital Storytelling',
                 'Digital Publishing',
                 'Mapping and Spatial Analysis', # GIS
                 'Metadata',
                 'Project Managment',
                 'Text Mining and Analysis',
                 'Web Development',
                 'Other'
                 ]
