from neo4j import GraphDatabase

def get_list_nodes(url, username,password, database):
    query = """
            MATCH (n)
            WITH DISTINCT labels(n) AS labels
            UNWIND labels AS label
            RETURN DISTINCT label
            ORDER BY label
            """
    driver = GraphDatabase.driver(uri=url, auth=(username, password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        list_labels = []
        for record in result:
            list_labels.append(record.data()['label'])
    return list_labels

def get_list_relationship(url, username, password, database):
    query = """
            MATCH (a)-[r]->(b)
            RETURN DISTINCT type(r) AS TYPE
            """
    driver = GraphDatabase.driver(uri=url, auth=(username, password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        list_types = []
        for record in result:
            list_types.append(record.data()['TYPE'])
    return list_types

def match_nodes(url, username, password, database, NODE_1,NODE_2,RELATIONSHIP):
    query = """
            MATCH (a:{}) - [:{}]->(b:{})
            RETURN id(a) AS SOURCE_ID, id(b) AS TARGET_ID, a.name AS NODE1_LABEL, b. AS NODE2_LABEL
            """.format(NODE_1, RELATIONSHIP, NODE_2)
    driver = GraphDatabase.driver(uri=url, auth=(username, password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        source_id = []
        target_id = []
        source_label = []
        target_label = []
        for record in result:
            source_id.append(record.data()['SOURCE_ID'])
            target_id.append(record.data()['TARGET_ID'])
            source_label.append(record.data()['NODE1_LABEL'])
            target_label.append(record.data()['NODE2_LABEL'])
    return source_id,target_id, source_label, target_label

#####################################
def get_nodes_property(url,username, password, database, NODE_1, NODE_2, RELATIONSHIP):
    query = """
            MATCH (n:{})
            RETURN properties(n) AS PROPERTY    
            """.format(NODE_1)
    driver = GraphDatabase.driver(uri=url, auth=(username, password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        list_properties = []
        for record in result:
            list_properties.append(record.data()['PROPERTY'])
    keys = list(list_properties[0].keys())
    return keys, list_properties

def get_all_properties(url,username,password,database,NODE_1, NODE_2, RELATIONSHIP):
    query = """
            MATCH (a:{})-[r:{}]->(b:{})
            RETURN a.device AS S_DEVICE, a.ip AS S_IP, a.name AS S_NAME, a.latitude AS S_LATITUDE,
            a.longitude AS S_LONGITUDE, b.device AS T_DEVICE, b.ip AS T_IP, b.name AS T_NAME,
            b.latitude AS T_LATITUDE, b.longitude AS T_LONGITUDE
            """.format(NODE_1, RELATIONSHIP, NODE_2)
    driver = GraphDatabase.driver(uri=url, auth=(username,password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        list_properties = []
        for record in result:
            list_properties.append(record.data())
    
    return list_properties

# url = 'bolt://localhost:7687'
# username = 'neo4j'
# password = '12345678'
# db = 'neo4j'
# node1,node2,rel = 'OLT','ME','LINK'
# matchNodes = get_all_properties(url=url, username=username, password=password, database=db,NODE_1=node1,
#                          NODE_2=node2,RELATIONSHIP=rel)
# print(matchNodes[:2])
# output : {'S_DEVICE': 'OLT', 'S_IP': '192.168.10.51', 'S_NAME': 'OLT51', 'S_LATITUDE': '-7.291876', 
# 'S_LONGITUDE': '112.795481', 'T_DEVICE': 'ME', 'T_IP': '192.168.20.1', 'T_NAME': 'ME1', 'T_LATITUDE': '-7.316107', 
# 'T_LONGITUDE': '112.725496'}
def get_properties_one(url,username,password,database,NAME_NODE):
    query = """
            MATCH (n)
            WHERE n.name = '{}'
            RETURN n
            """.format(NAME_NODE)
    driver = GraphDatabase.driver(uri=url, auth=(username, password))
    with driver.session(database=database) as session:
        result = session.run(query=query)
        return result.data()[0]['n']

