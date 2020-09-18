from typing import List

import neo4j

from models.edge_model import EdgeModel
from models.node_model import NodeModel
from utils.singleton import Singleton

first_mock_graph = [
    EdgeModel(
        ['Loves'],
        NodeModel(neo4j.data.Node(graph=None, n_id='1', n_labels={'PC'}, properties=dict(a='13', b='24'))),
        NodeModel(neo4j.data.Node(graph=None, n_id='1', n_labels={'PC'}, properties=dict(a='32', b='44')))),
    EdgeModel(
        ['Hates'],
        NodeModel(neo4j.data.Node(graph=None, n_id='1', n_labels={'PC'}, properties=dict(a='13', b='24'))),
        NodeModel(neo4j.data.Node(graph=None, n_id='3', n_labels={'PC'}, properties=dict(a='c3', b='d4')))
    )
]
second_mock_graph = [
    EdgeModel(
        ['Kill'],
        NodeModel(
            neo4j.data.Node(graph=None, n_id='1', n_labels={'Peer'}, properties=dict(height='175', hobby='guitar'))
        ),
        NodeModel(
            neo4j.data.Node(graph=None, n_id='1', n_labels={'Jessica'}, properties=dict(height='170', hobby='dancing'))
        )
    ),
    EdgeModel(
        ['Marry'],
        NodeModel(
            neo4j.data.Node(graph=None, n_id='1', n_labels={'Peer'}, properties=dict(height='175', hobby='guitar'))
        ),
        NodeModel(
            neo4j.data.Node(graph=None, n_id='3', n_labels={'Miri'}, properties=dict(height='158', hobby='politics'))
        )
    ),
    EdgeModel(
        ['Mate'],
        NodeModel(
            neo4j.data.Node(graph=None, n_id='1', n_labels={'Peer'}, properties=dict(height='175', hobby='guitar'))),
        NodeModel(
            neo4j.data.Node(graph=None, n_id='3', n_labels={'Liron'}, properties=dict(height='165', hobby='singing')))
    )
]


class GraphController(metaclass=Singleton):
    def __init__(self, db_path) -> None:
        # TODO: add connection to db mechanism
        pass

    def get_graph(self, project_name: str) -> List[EdgeModel]:
        return first_mock_graph

    def update_graph(self, project_name: str, edges: List[EdgeModel]) -> List[EdgeModel]:
        return first_mock_graph

    def add_graph(self, project_name: str, edges: List[EdgeModel]):
        return first_mock_graph

    def get_matching_graphs(self, edges: List[EdgeModel]) -> List[List[EdgeModel]]:
        return [first_mock_graph, second_mock_graph]

    def get_project_name(self, project_id: int) -> str:
        return 'TKVHGS'
