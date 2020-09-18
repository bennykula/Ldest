import logging
from typing import List, Union

import neo4j
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from data_access_layer.abstract_db_contoller import AbstractDbController
from models.edge_model import EdgeModel
from models.node_model import NodeModel


class Neo4jDbController(AbstractDbController):
    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self) -> None:
        self._driver.close()

    def create(self, create_query: str) -> List[Union[NodeModel, EdgeModel]]:
        with self._driver.session() as session:
            result = session.write_transaction(self._create_transaction_function, create_query)
            return result

    @staticmethod
    def _create_transaction_function(tx, create_query: str) -> List[Union[NodeModel, EdgeModel]]:
        create_transaction_result = tx.run(create_query)
        try:
            return Neo4jDbController._generate_nodes_and_edges_list(create_transaction_result)
        except ServiceUnavailable as exception:
            logging.error(f"{create_query} raised an error: \n {exception}")
            raise

    def match(self, match_query: str) -> List[Union[NodeModel, EdgeModel]]:
        with self._driver.session() as session:
            result = session.read_transaction(self._match_transaction_function, match_query)
            return result

    @staticmethod
    def _match_transaction_function(tx, match_query: str) -> List[Union[NodeModel, EdgeModel]]:
        match_transaction_result = tx.run(match_query)
        return Neo4jDbController._generate_nodes_and_edges_list(match_transaction_result)

    @staticmethod
    def _generate_nodes_and_edges_list(transaction_result: neo4j.Result) -> List[Union[NodeModel, EdgeModel]]:
        result = []
        for record in transaction_result:
            for item in record.items():
                entity = item[1]
                if isinstance(entity, neo4j.data.Node):
                    result.append(NodeModel(entity))
                elif isinstance(entity, neo4j.data.Relationship):
                    result.append(EdgeModel({entity.type}, NodeModel(entity.nodes[0]), NodeModel(entity.nodes[1])))
        return result
