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
