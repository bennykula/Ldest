from dataclasses import dataclass
from typing import Dict, List

import neo4j


@dataclass
class NodeModel:
    id: str  # MAC
    labels: List[str]
    properties: Dict[str, str]

    def __init__(self, neo4j_node: neo4j.data.Node):
        self.id = neo4j_node.id
        self.labels = list(set(neo4j_node.labels))
        self.properties = dict(neo4j_node._properties)

    @classmethod
    def from_dict(cls, node_model_dict: Dict[str, any]):
        return cls(neo4j.data.Node(
            graph=None,
            n_id=node_model_dict['id'],
            n_labels=node_model_dict['labels'],
            properties=node_model_dict['properties']
        ))
