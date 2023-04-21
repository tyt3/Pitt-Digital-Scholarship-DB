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
    'proficiency_level': [
        'Fundamental Awareness (basic knowledge)',
        'Novice (limited experience)',
        'Intermediate (practical application)',
        'Advanced (applied theory)',
        'Expert (recognized authority)'
        ],
    'subunit_type': [
        'Group',
        'Lab',
        'Library',
        'Office',
        'Team',
        'Unit',
        'Other'
        ],
    'superior': [
        'department',
        'subunit'
        ],
    'support_type': [
        'Collaboratory only',
        'Formal',
        'Informal'
        ]
}

existing = {
    'areas': list(zip(*db_session.query(Area.area_name).distinct()))[0],
    'campuses': list(zip(*db_session.query(Address.campus).distinct()))[0],
    'career_levels': list(zip(*db_session.query(Funding.career_level).distinct()))[0],
    'funding_types': list(zip(*db_session.query(Funding.funding_type).distinct()))[0],
    'payment_types': list(zip(*db_session.query(Funding.payment_type).distinct()))[0],
    'methods': list(zip(*db_session.query(Method.method_name).distinct()))[0],
    'resources': list(zip(*db_session.query(Resource.resource_type).distinct()))[0],
    'support_types': list(zip(*db_session.query(Person.support_type).distinct()))[0],
    'tools': list(zip(*db_session.query(Tool.tool_name).distinct()))[0],
    'units': list(zip(*db_session.query(Unit.unit_name).distinct()))[0],
    'departments': None,
    'subunits': list(zip(*db_session.query(Subunit.subunit_name).distinct()))[0]
}

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
