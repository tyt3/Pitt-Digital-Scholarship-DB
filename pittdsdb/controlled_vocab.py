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
        'Any',
        'Doctoral',
        'Graduate',
        'Masters',
        'Postdoctoral',
        'Postgraduate',
        'Professional',
        'Secondary School',
        'Undergraduate',
        'Other'
        ],
    'duration': [
        'Academic Year',
        'Calendar Year',
        'Fall Semester',
        'Multi-year',
        'Spring Semester',
        'Summer',
        'Other'
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
        'Graduate Student Assistantship',
        'Grant',
        'Internship',
        'Graduate Research Assistantship',
        'Scholarship',
        'Undergraduate Research Assistantship',
        'Undergraduate Student Assistantship',
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
        'Institute',
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
        'Web Browser Application',
        'Web Browser Plugin',
        'Other'
    ],
}

# Get entity values
areas = None
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

durations = None
try:
    durations= list(zip(*db_session.query(Funding.duration).distinct()))[0]
except:
    pass

frequencies = None
try:
    frequencies = list(zip(*db_session.query(Funding.frequency).distinct()))[0]
except:
    pass

methods = None
try:
    methods = list(zip(*db_session.query(Method.method_name).distinct()))[0]
except:
    pass

resources = None
try:
    resources = list(zip(*db_session.query(Resource.resource_name).distinct()))[0]
except:
    pass

resource_types = None
try:
    resource_types = list(zip(*db_session.query(Resource.resource_type).distinct()))[0]
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

tool_types = None
try:
    tool_types = list(zip(*db_session.query(Tool.tool_type).distinct()))[0]
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
            durations, frequencies, methods, resources, resource_types,
            support_types, tools, tool_types, units, subunits]

existing = {
    'areas': [],
    'campuses': [],
    'career_levels': [],
    'funding_types': [],
    'payment_types': [],
    'durations': [],
    'frequencies': [],
    'methods': [],
    'resources': [],
    'resource_types': [],
    'support_types': [],
    'tools': [],
    'tool_types': [],
    'units': [],
    'subunits': []
}

i = 0
for entity in existing:
    entity_values = entities[i]
    if entity_values:
        value_list = list(entity_values)
        value_list.sort()
        existing[entity] = value_list
    i += 1

all_units = existing['units'] + existing['subunits']
all_units.sort()
existing['all_units'] = all_units

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
