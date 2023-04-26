from .neo4j_database import neo4j_dbconn

def delete_node(entity, attribute, attribute_value):
    del_qry =  "MATCH (n:"+entity+") " \
                "WHERE "+attribute+" = '"+attribute_value+"' " \
                "DETACH DELETE n"  
    neo4j_dbconn.query(del_qry)


def get_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute):
    get_relations_qry = "MATCH (:"+from_entity+" {"+from_unique_attribute+": '"+from_unique_attribute_value+"'})-[r]->(t:"+to_entity+") RETURN t."+to_unique_attribute
    result = neo4j_dbconn.query(get_relations_qry)
    return result

def add_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute, to_unique_attribute_value, relation_name, reverse_relation_name):
    rel_cqry = "MATCH (f:"+from_entity+"{"+from_unique_attribute+": '"+from_unique_attribute_value+"'}), (t:"+to_entity+"{"+to_unique_attribute+": '"+to_unique_attribute_value+"'}) " \
               "CREATE (f)-[:"+relation_name+"]->(t)-[:"+reverse_relation_name+"]->(f)"
    print(rel_cqry)
    neo4j_dbconn.query(rel_cqry)

def detch_relations(from_entity, from_unique_attribute, from_unique_attribute_value, to_entity, to_unique_attribute, to_unique_attribute_value, relations):
    for relation in relations:
        rel_cqry = "MATCH (:"+from_entity+" {"+from_unique_attribute+": '"+from_unique_attribute_value+"'}) - [r:"+relation+"]-(:"+to_entity+" {"+to_unique_attribute+": '"+to_unique_attribute_value+"'}) DELETE r"
        neo4j_dbconn.query(rel_cqry)

def get(entity, attribute, attribute_value):
    get_qry = "MATCH (n:"+entity+" {"+attribute+": '"+attribute_value+"'}) " \
              "WITH n" \
              "RETURN n."+attribute
    result = neo4j_dbconn.query(get_qry)
    return result

###     PERSON

def add_person_node(name, public_id):
    profile_link = url_for('views_bp.view_person', public_id=public_id)
    person_cqry =  "CREATE (:Person {  public_id: '"+public_id+"', name: '"+name+"', profile: '" + profile_link + "'})"
    neo4j_dbconn.query(person_cqry)

def update_person_node(name, public_id):
    person_cqry =  "MATCH (p:Person) " \
                   "WHERE p.public_id = '"+public_id+"' " \
                   "SET p.name = '"+name+"'"
            
    neo4j_dbconn.query(person_cqry)

def attach_person_unit(public_id, unit):
    add_relations("Person", "public_id", public_id, "Unit", "public_id", unit, "PART_OF", "INCLUDES")

def attach_person_subunit(public_id, subunit):
    add_relations("Person", "public_id", public_id, "SubUnit", "public_id", subunit, "PART_OF", "INCLUDES")

def attach_person_area(public_id, area):
    add_relations("Person", "public_id", public_id, "Area", "name", area, "SUPPORTS", "SUPPORTED_BY")

def attach_person_method(public_id, method):
    add_relations("Person", "public_id", public_id, "Method", "name", method, "SUPPORTS", "SUPPORTED_BY")

def attach_person_tool(public_id, tool):
    add_relations("Person", "public_id", public_id, "Tool", "name", tool, "SUPPORTS", "SUPPORTED_BY")

def detach_person_unit(public_id, unit):
    detch_relations("Person", "public_id", public_id, "Unit", "public_id", unit ['PART_OF', 'INCLUDES'])

def detach_person_subunit(public_id, subunit):
    detch_relations("Person", "public_id", public_id, "SubUnit", "public_id", subunit, ['PART_OF', 'INCLUDES'])

def detach_person_area(public_id, area):
    detch_relations("Person", "public_id", public_id, "Area", "name", area, ['SUPPORTS', "SUPPORTED_BY"])

def detach_person_method(public_id, method):
    detch_relations("Person", "public_id", public_id, "Method", "name", method, ['SUPPORTS', "SUPPORTED_BY"])

def detach_person_tool(public_id, tool):
    detch_relations("Person", "public_id", public_id, "Tool", "name", tool, ['SUPPORTS', "SUPPORTED_BY"])
            
###     UNIT

def add_unit_node(public_id, name):
    profile_uri = url_for('views_bp.view_unit', public_id=public_id)
    unit_cqry =  "CREATE (:Unit {public_id:'" + public_id +"',  view_unit: '"+profile_uri+"', name: '"+name+"'})"
    neo4j_dbconn.query(unit_cqry)

def update_unit_node(public_id, name):
    unit_cqry =  "MATCH (u:Unit) " \
                 "WHERE u.public_id = '"+public_id+"' " \
                 "SET u.name = '"+name+"'"
            
    neo4j_dbconn.query(unit_cqry)

def attach_unit_subunit(unit, subunit):
    add_relations("Unit", "public_id", unit, "SubUnit", "public_id", unit, "HOUSES", "HOUSED_IN")

def attach_unit_resource(unit, resource):
    add_relations("Unit", "public_id", unit, "Resource", "public_id", subunit, "PROVIDES", "PROVIDED_BY")

def attach_unit_funding(unit, funding):
    add_relations("Unit", "public_id", unit, "Funding", "public_id", funding, "PROVIDES", "PROVIDED_BY")

def detach_unit_subunit(unit, subunit):
    detch_relations("Unit", "public_id", unit, "SubUnit", "public_id", area, ['HOUSES', "HOUSED_IN"])

def detach_unit_resource(unit, resource):
    detch_relations("Unit", "public_id", unit, "Resource", "name", resource, ["PROVIDES", "PROVIDED_BY"])

def detach_unit_funding(unit, funding):
    detch_relations("Unit", "public_id", unit, "Funding", "public_id", funding, ["PROVIDES", "PROVIDED_BY"])
 
###     SUBUNIT

def add_subunit_node(public_id, name, profile_uri, parent_node):
    unit_cqry =  "CREATE (:SubUnit {  public_id: '"+public_id+"', view_unit: '"+profile_uri+"', name: '"+name+"', parent_unit:'"+parent_node+"'})"
    neo4j_dbconn.query(unit_cqry)

def update_subunit_node(public_id, name):
    unit_cqry =  "MATCH (u:SubUnit) " \
                 "WHERE u.public_id = '"+public_id+"' " \
                 "SET u.name = '"+name+"'"
            
    neo4j_dbconn.query(unit_cqry)

def attach_subunit_resource(unit, resource):
    add_relations("SubUnit", "public_id", unit, "Resource", "public_id", subunit, "PROVIDES", "PROVIDED_BY")

def attach_subunit_funding(unit, funding):
    add_relations("SubUnit", "public_id", unit, "Funding", "public_id", funding, "PROVIDES", "PROVIDED_BY")

def detach_subunit_resource(unit, resource):
    detch_relations("SubUnit", "public_id", unit, "Resource", "name", resource, ["PROVIDES", "PROVIDED_BY"])

def detach_subunit_funding(unit, funding):
    detch_relations("SubUnit", "public_id", unit, "Funding", "public_id", funding, ["PROVIDES", "PROVIDED_BY"])
                    
###     AREA
                        

def add_area_node(name):
    person_cqry =  "CREATE (:Area { name: '"+name+"'})"
    neo4j_dbconn.query(person_cqry)

def attach_area_method(area, method):
    add_relations("Area", "name", area, "Method", "name", method, 'INCLUDES', 'INCLUDED_BY')

def attach_area_tool(area, tool):
    add_relations("Area", "name", area, "Tool", "name", tool, 'USES', 'USED_BY')

def attach_area_resource(area, resource):
    add_relations("Area", "name", area, "Resource", "name", resource, "USES", "USED_BY")

def detach_area_method(area, method):
    detch_relations("Area", "name", area, "Method", "name", method, ['INCLUDES', 'INCLUDED_BY'])

def detach_area_tool(area, tool):
    detch_relations("Area", "name", area, "Tool", "name", tool, ['USES', 'USED_BY'])

def detach_area_resource(area, resource):
    detch_relations("Area", "name", area, "Resource", "name", resource, ["USES", "USED_BY"])

###     METHOD

def add_method_node(name):
    method_cqry =  "CREATE (:Method { name: '"+name+"'})"
    neo4j_dbconn.query(method_cqry)

def attach_tool_method(tool, method):
    add_relations("Method", "name", method, "Tool", "name", tool, "USES", "USED_FOR")


def detach_tool_method(tool, method):
    detch_relations("Method", "name", method, "Tool", "name", tool, ['USES', 'USED_FOR'])

    
###     TOOL

def add_tool_node(name, web_address, github):
    tool_cqry =  "CREATE (:Tool { name: '"+name+"', web_address: '"+web_address+"', github: '"+github+"'})"
    neo4j_dbconn.query(tool_cqry)

    
def update_tool_node(name, web_address, github):
    tool_cqry =  "MATCH (t:Tool) " \
                 "WHERE t.name = '"+name+"' " \
                 "SET t.name = '"+name+"', t.web_address = '"+web_address+"', t.github = '"+github+"'"
            
    neo4j_dbconn.query(tool_cqry)


###     RESOURCE


def add_resource_node(name, resource_type):
    rsc_cqry =  "CREATE (:Resource { name: '"+name+"', type: '"+resource_type+"'})"
    neo4j_dbconn.query(rsc_cqry)

    
def update_resource_node(name, resource_type):
    rsc_cqry =  "MATCH (r:Resource) " \
                "WHERE r.name = '"+name+"' " \
                "SET r.name = '"+name+"', r.type = '"+resource_type+"'"
            
    neo4j_dbconn.query(rsc_cqry)


###     FUNDING


def add_funding_node(name, public_id):
    link = url_for('views_bp.view_funding', public_id=public_id)
    fund_cqry =  "CREATE (:Funding {  public_id: '"+public_id+"', name: '"+name+"', view_funding: '"+link+"'})"
    neo4j_dbconn.query(fund_cqry)
 
def update_funding_node(name, public_id):
    fund_cqry =  "MATCH (f:Funding) " \
                 "WHERE f.public_id = '"+public_id+"' " \
                 "SET f.name = '"+name+"'"  
    neo4j_dbconn.query(fund_cqry)

