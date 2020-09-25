import logging
from typing import List, Union

import neo4j
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from data_access_layer.abstract_db_contoller import AbstractDbController
from models.node_model import NodeModel

from models.relationship_model import RelationshipModel


# TODO: Rename better
class Neo4jDbController(AbstractDbController):
    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self) -> None:
        self._driver.close()

    def create(self, create_query: str) -> List[Union[NodeModel, RelationshipModel]]:
        with self._driver.session() as session:
            result = session.write_transaction(self._create_transaction_function, create_query)
            return result

    @staticmethod
    def _create_transaction_function(tx, create_query: str) -> List[Union[NodeModel, RelationshipModel]]:
        try:
            return Neo4jDbController._generic_transaction_function(tx, create_query)
        except ServiceUnavailable as exception:
            logging.error(f"{create_query} raised an error: \n {exception}")
            raise

    @staticmethod
    def _generic_transaction_function(tx, query: str) -> List[Union[NodeModel, RelationshipModel]]:
        transaction_result = tx.run(query)
        return Neo4jDbController._generate_nodes_and_edges_list(transaction_result)

    def match(self, match_query: str) -> List[Union[NodeModel, RelationshipModel]]:
        return self._run_read_query(match_query)

    def get_project_match(self, project_match_query: str) -> List[Union[NodeModel, RelationshipModel]]:
        return self._run_read_query(project_match_query)

    def _run_read_query(self, read_query: str) -> List[Union[NodeModel, RelationshipModel]]:
        with self._driver.session() as session:
            result = session.read_transaction(Neo4jDbController._generic_transaction_function, read_query)
            return result

    @staticmethod
    def _generate_nodes_and_edges_list(transaction_result: neo4j.Result) -> List[Union[NodeModel, RelationshipModel]]:
        result = []
        for record in transaction_result:
            for item in record.items():
                entity = item[1]
                if isinstance(entity, neo4j.data.Node):
                    result.append(NodeModel(entity))
                elif isinstance(entity, neo4j.data.Relationship):
                    result.append(RelationshipModel(entity))
        return result
