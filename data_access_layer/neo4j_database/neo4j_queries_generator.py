from typing import Dict, Iterable, Set

from models.edge_model import EdgeModel
from models.node_model import NodeModel


class Neo4jQueriesGenerator:
    def __init__(self, edges: Iterable[EdgeModel]):
        self._edges = edges

    def generate_creation_query(self) -> str:
        creation_query = f'CREATE '
        creation_query_variables = set()
        for edge in self._edges:
            creation_query_variables.add(self._variable_name(edge))
            node_queries = []
            for node in [edge.source_node, edge.destination_node]:  # NOTICE! the list's elements order is important!
                creation_query_variables.add(self._variable_name(node))

                should_generate_labels_and_properties_query = self._variable_name(node) not in creation_query_variables
                node_queries.append(self._generate_node_query(node, should_generate_labels_and_properties_query))

            # Concat the source node query and the destination node query using the relationship query
            relationship_query = f'-[{self._variable_name(edge)}:{":".join(edge.labels)}]->'
            creation_query += relationship_query.join(node_queries)
            creation_query += ', '

        creation_query = creation_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
        creation_query += f' RETURN {", ".join(creation_query_variables)}'
        return creation_query

    def _generate_node_query(self, node: NodeModel, should_generate_labels_and_properties_query: bool) -> str:
        """
        Generates a query related to the node part. For example, (id_2153351119296:Person:Murderer {id:'3'})
        :param creation_query_variables: A set of all
        :param node: The node to generate into a query
        :return: The node part of the cypher query
        """
        creation_query = f'({self._variable_name(node)}'
        if should_generate_labels_and_properties_query:
            properties_dict = node.properties
            properties_dict.update({'id': node.id})
            creation_query += self._generate_labels_and_properties_query(node.labels, properties_dict)
        creation_query += ')'
        return creation_query

    @staticmethod
    def _generate_labels_and_properties_query(labels: Iterable[str], properties: Dict[str, str]) -> str:
        labels_and_properties = f':{":".join(labels)}'
        if len(properties) > 0:
            labels_and_properties += Neo4jQueriesGenerator._generate_properties_query(properties)
        return labels_and_properties

    @staticmethod
    def _generate_properties_query(labels_dict: Dict[str, str]) -> str:
        labels_query = ' {'
        for label, value in labels_dict.items():
            labels_query += f"{label}:\'{value}\', "
        labels_query = labels_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
        labels_query += '}'
        return labels_query

    @staticmethod
    def _variable_name(obj: any) -> str:
        return 'id_' + str(id(obj))

    def generate_match_query(self) -> str:
        match_query = 'MATCH '
        connections = []
        match_query_variables = {
            self._variable_name(var) for edge in self._edges for var in [edge, edge.source_node, edge.destination_node]
        }
        for edge in self._edges:
            node_queries = []
            for node in [edge.source_node, edge.destination_node]:
                node_queries.append(
                    f'({self._variable_name(node)}'
                    f'{self._generate_labels_and_properties_query(node.labels, node.properties)})'
                )
            relationship_query = f'-[{self._variable_name(edge)}:{":".join(edge.labels)}]-'
            connection = relationship_query.join(node_queries)
            connections.append(connection)

        match_query += ', '.join(connections)
        match_query += f' RETURN {", ".join(match_query_variables)}'
        return match_query
