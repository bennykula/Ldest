from abc import abstractmethod
from typing import List, Union

from models.edge_model import EdgeModel
from models.node_model import NodeModel
from utils.abstact_class_singleton import AbstractClassSingleton


class AbstractDbController(metaclass=AbstractClassSingleton):
    @abstractmethod
    def create(self, create_query: str) -> List[Union[NodeModel, EdgeModel]]:
        pass

    @abstractmethod
    def match(self, match_query: str) -> List[Union[NodeModel, EdgeModel]]:
        pass
