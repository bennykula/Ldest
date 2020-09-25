from dataclasses import dataclass
from typing import Dict, List, Union

import neo4j


@dataclass
class RelationshipModel:
    labels: List[str]
    source_node_id: int
    destination_node_id: int

    def __init__(self, relationship_data: Union[neo4j.data.Relationship, Dict[str, any]]):
        if isinstance(relationship_data, neo4j.data.Relationship):
            self.labels = list({relationship_data.type})
            self.source_node_id = relationship_data.start_node._properties['id']
            self.destination_node_id = relationship_data.end_node._properties['id']
        elif isinstance(relationship_data, dict):
            self.labels = relationship_data['labels']
            self.source_node_id = relationship_data['source_node_id']
            self.destination_node_id = relationship_data['destination_node_id']
        else:
            pass  # TODO: Raise error
