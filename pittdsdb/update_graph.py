from .neo4j_database import neo4j_dbconn

def get_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute):
    get_relations_qry = "MATCH (:"+from_entity+" {"+from_unique_attribute+": '"+from_unique_attribute_value+"'})-[r]->(t:"+to_entity+") RETURN t."+to_unique_attribute
    result = neo4j_dbconn.query(get_relations_qry)
    return result

def add_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute, to_unique_attribute_value, relation_name, reverse_relation_name):
    rel_cqry = "MATCH (f:"+from_entity+"), (t:"+to_entity+") " \
               "WHERE f."+from_unique_attribute+" = '" + from_unique_attribute_value + "' AND t."+to_unique_attribute+" = '" + to_unique_attribute_value + "' " \
               "CREATE (f)-[:"+relation_name+"]->(t)," \
               "CREATE (f)<-[:"+reverse_relation_name+"]-(t)

    neo4j_dbconn.query(person_rel_cqry)

def detch_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute, to_unique_attribute_value, relations):
    for relation in relations:
        rel_cqry = "MATCH (:"+from_entity+" {"+from_unique_attribute+": '"+from_unique_attribute_value+"'}) - [r:"+relation+"]-(:"+to_entity+":{"+to_unique_attribute+": '"+to_unique_attribute_value+"'}) DELETE r"
        neo4j_dbconn.query(rel_cqry)

def get(entity, attribute, attribute_value):
    get_qry = "MATCH (n:"+entity+" {"+attribute+": '"+attribute_value+"'}) " \
              "WITH n" \
              "RETURN n."+attribute
    result = neo4j_dbconn.query(get_qry)
    return result

###     PERSON
        
def add_person(person_name, public_id, units, subunits, areas, tools, methods):
    link = url_for('views_bp.view_person', public_id=public_id)
    add_person_node(person_name, public_id, link)
    
    for area in areas:
        add_relations("Person", "public_id", public_id, "Area", "name", area, "SUPPORTS", "SUPPORTED_BY")

    for tool in tools:
        add_relations("Person", "public_id", public_id, "Tool", "name", tool, "SUPPORTS", "SUPPORTED_BY")

    for method in methods:
        add_relations("Person", "public_id", public_id, "Method", "name", method, "SUPPORTS", "SUPPORTED_BY")
                        
    for unit in units:
        add_relations("Person", "public_id", public_id, "Unit", "public_id", unit, "PART_OF", "INCLUDES")
                        
    for subunit in subunits:
        add_relations("Person", "public_id", public_id, "SubUnit", "public_id", subunit, "PART_OF", "INCLUDES")

def add_person_node(name, public_id, profile_link):
    person_cqry =  "CREATE (:Person {  public_id: '"+public_id+"', name: '"+name+"', profile: '" + profile_link + "'})"
    neo4j_dbconn.query(person_cqry)
    percons_cqry  = "CREATE CONSTRAINT ON (p:Person) ASSERT p.public_id IS UNIQUE"
    neo4j_dbconn.query(percons_cqry)

    
def update_person(public_id, units, subunits, areas, tools, methods):
    person_cqry =  "MATCH (:Person) " \
                   "WHERE public_id = '"+public_id+"' " \
                   "SET name = '"+last_name+", "+first_name+"'"
            
    neo4j_dbconn.query(person_cqry)

    relations = get_relations("Person", "public_id", public_id, "Unit", "public_id")
    for relation in relations:
        if relation not in units:
            detch_relations("Person", "public_id", public_id, "Unit", "public_id", relation ['PART_OF', 'INCLUDES'])

    relations = get_relations("Person", "public_id", public_id, "SubUnit", "public_id")
    for relation in relations:
        if relation not in subunits:
            detch_relations("Person", "public_id", public_id, "SubUnit", "public_id", relation, ['PART_OF', 'INCLUDES'])

    relations = get_relations("Person", "public_id", public_id, "Area", "name")        
    for relation in relations:
        if relation not in areas:
            detch_relations("Person", "public_id", public_id, "Area", "name", relation, ['SUPPORTS', "SUPPORTED_BY"])

    relations = get_relations("Person", "public_id", public_id, "Method", "name")
    for relation in relations:
        if relation not in tools:
            detch_relations("Person", "public_id", public_id, "Method", "name", relation, ['SUPPORTS', "SUPPORTED_BY"])

    relations = get_relations("Person", "public_id", public_id, "Tool", "name")
    for relation in relations:
        if relation not in methods:
            detch_relations("Person", "public_id", public_id, "Tool", "name", relation, ['SUPPORTS', "SUPPORTED_BY"])

###     UNIT

def add_unit(unit_name, public_id, subunits, resources, fundings):
    link = url_for('views_bp.view_unit', public_id=public_id)
    add_unit_node(public_id, unit_name, link, len(subunits))
                        
    for subunit in subunits:
        add_relations("Unit", "public_id", public_id, "SubUnit", subunit, "public_id", "HOUSES", "HOUSED_IN")
        
    for resource in resources:
        add_relations("Unit", "public_id", public_id, "Resource", resource, "name", "PROVIDES", "PROVIDED_BY")
        
    for funding in fundings:
        add_relations("Unit", "public_id", public_id, "Funding", funding, "public_id", "OFFERS", "OFFERED_BY")

def add_unit_node(public_id, name, profile_uri, num_subunits):
    unit_cqry =  "CREATE (:Unit {public_id:'" + public_id +"',  view_unit: '"+profile_uri+"', name: '"+name+"', num_units:'"+num_subunits+"'})"
    neo4j_dbconn.query(unit_cqry)
    unitcons_cqry  = "CREATE CONSTRAINT ON (u:Unit) ASSERT u.public_id IS UNIQUE"
    neo4j_dbconn.query(unitcons_cqry)

    
def update_unit(public_id, name, subunits, resources, fundings):
    unit_cqry =  "MATCH (:Unit) " \
                 "WHERE public_id = '"+public_id+"' " \
                 "SET name = '"+name+"', num_units = '"+len(subunits)
            
    neo4j_dbconn.query(unit_cqry)

    relations = get_relations("Unit", "public_id", public_id, "SubUnit", "public_id")
    for relation in relations:
        if relation not in subunits:
            detch_relations("Unit", "public_id", public_id, "SubUnit", "public_id", relation, ["HOUSES", "HOUSED_IN"])

    relations = get_relations("Unit", "public_id", public_id, "Resource", "name")        
    for relation in relations:
        if relation not in resources:
            detch_person_relations("Unit", "public_id", public_id, "Resource", "name", relation, ['PROVIDES', 'PROVIDED_BY'])

    relations = get_relations("Unit", "public_id", public_id, "Funding", "public_id")
    for relation in relations:
        if relation not in fundings:
            detch_person_relations("Unit", "public_id", public_id, "Funding", "public_id", relation, ['PROVIDES', 'PROVIDED_BY'])


###     SUBUNIT

def add_subunit(sub_unit_name, public_id, unit_name, resources, fundings):
    link = url_for('views_bp.view_unit', public_id=public_id)
    add_subunit_node(sub_unit_name, public_id, unit_name)
    
    for resource in resources:
        add_relations("Unit", "public_id", public_id, "Resource", resource, "name", "PROVIDES", "PROVIDED_BY")
        
    for funding in fundings:
        add_relations("Unit", "public_id", public_id, "Funding", funding, "public_id", "OFFERS", "OFFERED_BY")

def add_subunit_node(public_id, name, profile_uri, parent_node):
    unit_cqry =  "CREATE (:SubUnit {  public_id: '"+public_id+"', view_unit: '"+profile_uri+"', name: '"+name+"', parent_unit:'"+parent_node+"'})"
    neo4j_dbconn.query(unit_cqry)
    unitcons_cqry  = "CREATE CONSTRAINT ON (u:SubUnit) ASSERT u.public_id IS UNIQUE"
    neo4j_dbconn.query(unitcons_cqry)

    
def update_subunit(public_id, name):
    unit_cqry =  "MATCH (:SubUnit) " \
                 "WHERE public_id = '"+public_id+"' " \
                 "SET name = '"+name+"'"
            
    neo4j_dbconn.query(unit_cqry)

    relations = get_relations("Unit", "public_id", public_id, "Resource", "name")        
    for relation in relations:
        if relation not in resources:
            detch_person_relations("Unit", "public_id", public_id, "Resource", "name", relation, ['PROVIDES', 'PROVIDED_BY'])

    relations = get_relations("Unit", "public_id", public_id, "Funding", "public_id")
    for relation in relations:
        if relation not in fundings:
            detch_person_relations("Unit", "public_id", public_id, "Funding", "public_id", relation, ['PROVIDES', 'PROVIDED_BY'])

###     AREA

def add_area(area_name, methods, tools, resources):
    add_area_node(area_name)
    
    for tool in tools:
        add_relations("Area", "name", area_name, "Tool", "name", tool, "USES", "USED_FOR")

    for method in methods:
        add_relations("Area", "name", area_name, "Method", "name", method, "INCLUDED", "TYPE_OF")
                        
    for resource in resources:
        add_relations("Area", "name", area_name, "Resource", "name", resource, "USES", "USED_FOR")
                        

def add_area_node(name):
    person_cqry =  "CREATE (:Area { name: '"+name+"'})"
    neo4j_dbconn.query(person_cqry)
    percons_cqry  = "CREATE CONSTRAINT ON (a:Area) ASSERT a.name IS UNIQUE"
    neo4j_dbconn.query(percons_cqrypercons_cqry)

    
def update_area(name, methods, tools, resources):
    area_cqry =  "MATCH (:Area) " \
                   "WHERE area = '"+name+"' " \
                   "SET name = '"+name+"'"
            
    neo4j_dbconn.query(area_cqry)

    relations = get_relations("Area", "name", name, "Method", "name")
    for relation in relations:
        if relation not in methods:
            detch_relations("Area", "name", name, "Method", "name", relation, ['INCLUDES', 'INCLUDED_BY'])

    relations = get_relations("Area", "name", name,, "Tool", "name")
    for relation in relations:
        if relation not in tools:
            detch_relations("Area", "name", name, "Tool", "name", relation, ['USES', 'USED_BY'])

###     METHOD

def add_method(method_name, tools):
    add_method_node(method_name)

    for tool in tools:
        add_relations("Method", "name", method_name, "Tool", "name", tool, "USES", "USED_FOR")

def add_method_node(name):
    method_cqry =  "CREATE (:Method { name: '"+name+"'})"
    neo4j_dbconn.query(method_cqry)
    methcons_cqry  = "CREATE CONSTRAINT ON (m:Method) ASSERT m.name IS UNIQUE"
    neo4j_dbconn.query(methcons_cqry)

def update_method(name, tools):
    method_cqry =  "MATCH (:Method) " \
                   "WHERE name = '"+name+"' " \
                   "SET name = '"+name+"'"
            
    neo4j_dbconn.query(method_cqry)

    relations = get_relations("Method", "name", name, "Tool", "name")
    for relation in relations:
        if relation not in tools:
            detch_relations("Method", "name", name, "Tool", "name", relation, ['USES', 'USED_FOR'])

###     TOOL

def add_tool(tool_name):
    add_tool_node(tool_name)


def add_tool_node(name):
    tool_cqry =  "CREATE (:Tool { name: '"+name+"'})"
    neo4j_dbconn.query(tool_cqry)
    tcons_cqry  = "CREATE CONSTRAINT ON (t:Tool) ASSERT t.name IS UNIQUE"
    neo4j_dbconn.query(tcons_cqry)

    
def update_tool(name):
    tool_cqry =  "MATCH (:Tool) " \
                 "WHERE name = '"+name+"' " \
                 "SET name = '"+name+"'"
            
    neo4j_dbconn.query(tool_cqry)


###     RESOURCE

def add_resource(resource_name):
    add_resource_node(resource_name)


def add_resource_node(name):
    rsc_cqry =  "CREATE (:Resource { name: '"+name+"'})"
    neo4j_dbconn.query(rsc_cqry)
    rsccons_cqry  = "CREATE CONSTRAINT ON (r:Resource) ASSERT r.name IS UNIQUE"
    neo4j_dbconn.query(rsccons_cqry)

    
def update_resource(name):
    rsc_cqry =  "MATCH (:Resource) " \
                   "WHERE name = '"+name+"' " \
                   "SET name = '"+name+"'"
            
    neo4j_dbconn.query(rsc_cqry)


###     FUNDING

def add_funding(funding_name, public_id):
    link = url_for('views_bp.view_person', public_id=public_id)
    add_funding_node(funding_name, public_id, link)

def add_funding_node(name, public_id, link):
    fund_cqry =  "CREATE (:Funding {  public_id: '"+public_id+"', name: '"+name+"', view_funding: '"+link+"'})"
    neo4j_dbconn.query(fund_cqry)
    fundcons_cqry  = "CREATE CONSTRAINT ON (f:Funding) ASSERT f.public_id IS UNIQUE"
    neo4j_dbconn.query(fundcons_cqry)
 
def update_funding(name, public_id):
    person_cqry =  "MATCH (:Funding) " \
                   "WHERE public_id = '"+public_id+"' " \
                   "SET name = '"+last_name+"'"
            
    neo4j_dbconn.query(person_cqry)
