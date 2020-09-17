from dataclasses import dataclass
from typing import Iterable, List

from models.node_model import NodeModel


@dataclass
class EdgeModel:
    labels: List[str]
    source_node: NodeModel
    destination_node: NodeModel

    def __init__(self, labels: Iterable[str], source_node: NodeModel, destination_node: NodeModel):
        self.labels = list(set(labels))
        self.source_node = source_node
        self.destination_node = destination_node
