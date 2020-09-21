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
                'id': '1',
                'labels': {'PC'},
                'properties': dict(a='13', b='24')
            },
            'destination_node': {
                'id': '2',
                'labels': {'PC'},
                'properties': dict(a='32', b='44')
            }
        }
    ),
    EdgeModel(
        {
            'labels': ['Hates'],
            'source_node': {
                'id': '1',
                'labels': {'PC'},
                'properties': dict(a='13', b='24')
            },
            'destination_node': {
                'id': '3',
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
        return first_mock_graph

    def update_graph(self, project_name: str, edges: List[EdgeModel]) -> List[EdgeModel]:
        return first_mock_graph

    def add_graph(self, project_name: str, edges: List[EdgeModel]):
        return first_mock_graph

    def get_project_name(self, project_id: int) -> str:
        return 'TKVHGS'
