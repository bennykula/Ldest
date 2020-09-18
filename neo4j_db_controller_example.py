from data_access_layer.neo4j_database.neo4j_db_controller import Neo4jDbController

if __name__ == "__main__":
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 7687
    url = f"{scheme}://{host_name}:{port}"
    user = "neo4j"
    password = "123456"
    neo4j_db_controller = Neo4jDbController(url, user, password)

    print(neo4j_db_controller.create(
        "CREATE (id_1622478615120:Person {id:'1'})-[id_1622480956624:FRIENDS]->(id_1622481002752:Person:Swedish {"
        "name:'Andy', title:'Developer', id:'2'}), (id_1622478615120)-[id_1622480957056:ENEMIES]->("
        "id_1622480954272:Person:Murderer {id:'3'}) RETURN id_1622481002752, id_1622478615120, id_1622480957056, "
        "id_1622480956624, id_1622480954272 "
    ))
    print("\n" * 2)
    print(neo4j_db_controller.match(
        "MATCH (id_1622478615120:Person {id:'1'})-[id_1622480956624:FRIENDS]-(id_1622481002752:Person:Swedish {"
        "name:'Andy', title:'Developer', id:'2'}), (id_1622478615120:Person {id:'1'})-[id_1622480957056:ENEMIES]-("
        "id_1622480954272:Person:Murderer {id:'3'}) RETURN id_1622481002752, id_1622480956624, id_1622480954272, "
        "id_1622480957056, id_1622478615120 "
    ))
