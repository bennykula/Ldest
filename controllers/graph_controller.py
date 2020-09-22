from typing import List, Union

from data_access_layer.neo4j_database.neo4j_db_controller import Neo4jDbController
from data_access_layer.neo4j_database.neo4j_queries_generator import Neo4jQueriesGenerator
from models.edge_model import EdgeModel
from models.node_model import NodeModel
from utils.singleton import Singleton

first_mock_graph = [
    EdgeModel(
        {
            'labels': ['Loves'],
            'source_node': {
                'id': '12222222222222',
                'labels': {'PC'},
                'properties': dict(a='13', b='24')
            },
            'destination_node': {
                'id': '9999999999999992',
                'labels': {'PC'},
                'properties': dict(a='32', b='44')
            }
        }
    ),
    EdgeModel(
        {
            'labels': ['Hates'],
            'source_node': {
                'id': '1333333333333333333',
                'labels': {'PC'},
                'properties': dict(a='13', b='24')
            },
            'destination_node': {
                'id': '9999999999999993',
                'labels': {'PC'},
                'properties': dict(a='c3', b='d4')
            }
        }
    )
]


class GraphController(metaclass=Singleton):
    def __init__(self) -> None:
        scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
        host_name = "localhost"
        port = 7687
        uri = f"{scheme}://{host_name}:{port}"
        user = "neo4j"
        password = "123456"
        self._db_controller = Neo4jDbController(uri, user, password)

    def get_graph(self, project_name: str) -> List[EdgeModel]:
        project_match_query = Neo4jQueriesGenerator().generate_project_match_query(project_name)
        return self._db_controller.get_project_match(project_match_query)

    def update_graph(self, project_name: str, edges: List[EdgeModel]) -> List[EdgeModel]:
        update_graph_query = ''
        return first_mock_graph

    def add_graph(self, project_name: str, edges: List[EdgeModel]) -> List[Union[NodeModel, EdgeModel]]:
        for edge in edges:
            edge.source_node.properties.update({'project_name': project_name})
            edge.destination_node.properties.update({'project_name': project_name})
        create_query = Neo4jQueriesGenerator().generate_create_query(edges)
        return self._db_controller.create(create_query)

    def get_matching_graphs(self, edges: List[EdgeModel]) -> List[Union[NodeModel, EdgeModel]]:
        match_query = Neo4jQueriesGenerator().generate_match_query(edges)
        return self._db_controller.match(match_query)

