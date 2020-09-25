from dataclasses import dataclass
from typing import List

from models.node_model import NodeModel
from models.relationship_model import RelationshipModel


@dataclass
class GraphUpdateRequestModel:
    nodes_to_add: List[NodeModel]
    nodes_to_update: List[NodeModel]
    nodes_to_delete: List[NodeModel]
    relationships_to_add: List[RelationshipModel]
    relationships_to_update: List[RelationshipModel]
    relationships_to_delete: List[RelationshipModel]
