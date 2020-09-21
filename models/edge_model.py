from dataclasses import dataclass
from typing import Dict, Iterable, List

import neo4j

from models.node_model import NodeModel


@dataclass
class EdgeModel:
    labels: List[str]
    source_node: NodeModel
    destination_node: NodeModel

    def __init__(self, edge_dict: Dict[str, any]):
        self.labels = list(edge_dict['labels'])
        source_node_dict = edge_dict['source_node']
        self.source_node = NodeModel(
            neo4j.data.Node(
                graph=None,
                n_id=source_node_dict['id'],
                n_labels=source_node_dict['labels'],
                properties=source_node_dict['properties']
            )
        )
        destination_node_dict = edge_dict['destination_node']
        self.destination_node = NodeModel(
            neo4j.data.Node(
                graph=None,
                n_id=destination_node_dict['id'],
                n_labels=destination_node_dict['labels'],
                properties=destination_node_dict['properties']
            )
        )

    @classmethod
    def to_edge_model(cls, labels: Iterable[str], source_node: NodeModel, destination_node: NodeModel):
        return cls({
            'labels': labels,
            'source_node': {
                'id': source_node.id,
                'labels': source_node.labels,
                'properties': source_node.properties
            },
            'destination_node': {
                'id': destination_node.id,
                'labels': destination_node.labels,
                'properties': destination_node.properties
            }
        })
