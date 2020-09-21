from typing import Dict, Iterable, Set, Union

from models.edge_model import EdgeModel
from models.node_model import NodeModel


class Neo4jQueriesGenerator:
    def __init__(self, edges: Iterable[EdgeModel]):
        self._edges = edges

    def generate_create_query(self) -> str:
        """
        Generates a creation query
        :return: The creation query
        """
        creation_query = f'CREATE '
        connection_queries = []
        creation_query_variables = set()
        for edge in self._edges:
            connection_query = self._generate_connection_query(edge, creation_query_variables, True)
            connection_queries.append(connection_query)
            creation_query_variables |= {
                self._variable_name(x)
                for x in [edge, edge.source_node, edge.destination_node]
            }
        creation_query += ', '.join(connection_queries)
        creation_query += f' RETURN {", ".join(creation_query_variables)}'
        return creation_query

    def _generate_connection_query(self,
                                   edge: EdgeModel,
                                   dismiss_labels_and_properties_variables: Set[str],
                                   is_relationship_directed=False) -> str:
        """
        Generates the connection query part of the cypher query, for example:
        1. (a:Person {id:'1'})-[b:FRIENDS]->(c:Swedish:Person {name:'Andy', title:'Developer', id:'2'})
        2. (c:Person)-[b:FRIENDS]-(:Swedish)
        :param edge: The edge which will be described in the connection query
        :param dismiss_labels_and_properties_variables: Variables which we want to dismiss their labels and properties
        in the connection query
        :param is_relationship_directed: Whether the query related to a directed relationship or not
        :return: A connection query, for example, (c:Person)-[b:FRIENDS]-(:Swedish)
        """
        source_node_query = self._generate_node_query(
            edge.source_node,
            self._variable_name(edge.source_node) not in dismiss_labels_and_properties_variables
        )
        destination_node_query = self._generate_node_query(
            edge.destination_node,
            self._variable_name(edge.destination_node) not in dismiss_labels_and_properties_variables
        )
        relationship_query = self._generate_relationship_query(edge, is_relationship_directed)
        connection_query = relationship_query.join([source_node_query, destination_node_query])
        return connection_query

    def _generate_relationship_query(self, edge: EdgeModel, is_relationship_directed=False) -> str:
        """
        Generates a relationship query using the edge and the relationship type:
        1. Directed: (source) -> (destination)
        2. Not directed: (source) -- (destination)
        :param edge: The edge to be used in the relationship query
        :param is_relationship_directed: Whether the query related to a directed relationship or not
        :return: The relationship query, for example, -[:FRIENDS]- OR -[:HATES]->
        """
        if is_relationship_directed:
            relationship_query = f'-[{self._variable_name(edge)}:{":".join(edge.labels)}]->'
        else:
            relationship_query = f'-[{self._variable_name(edge)}:{":".join(edge.labels)}]-'
        return relationship_query

    def _generate_node_query(self, node: NodeModel, should_generate_labels_and_properties_query: bool) -> str:
        """
        Generates a query related to the node part. For example, (id_2153351119296:Person:Murderer {id:'3'})
        :param should_generate_labels_and_properties_query: Self explanatory
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
        """
        Generate the labels and properties part of the cypher query, for example:
        1. :Swedish:Person {name:'Andy', title:'Developer', id:'2'})
        2. :Person {id:'1'}
        :param labels: The labels to be described in the cypher query
        :param properties: The properties to be described in the cypher query
        :return: The labels and properties query, for example, :Person {id:'1'}
        """
        labels_and_properties = f':{":".join(labels)}'
        if len(properties) > 0:
            labels_and_properties += Neo4jQueriesGenerator._generate_properties_query(properties)
        return labels_and_properties

    @staticmethod
    def _generate_properties_query(properties: Dict[str, str]) -> str:
        """
        Generates the properties part of the cypher query, for example:
        1. {name:'Andy', title:'Developer', id:'2'}
        :param properties: The properties to be described in the cypher query
        :return: The properties query, for example, {name:'Andy', title:'Developer', id:'2'}
        """
        labels_query = ' {'
        for label, value in properties.items():
            labels_query += f"{label}:\'{value}\', "
        labels_query = labels_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
        labels_query += '}'
        return labels_query

    @staticmethod
    def _variable_name(obj: Union[EdgeModel, NodeModel]) -> str:
        """
        Returns a unique variable name to be used on the cypher query
        :param obj: The object we want to have unique variable name in the query
        :return: Unique variable name
        """
        if isinstance(obj, NodeModel):
            return f'id_{obj.id}'
        elif isinstance(obj, EdgeModel):
            return f'id_{id(obj)}'

    def generate_match_query(self) -> str:
        """
        Generates a match query
        :return: The match query
        """
        match_query = 'MATCH '
        connection_queries = []
        match_query_variables = {
            self._variable_name(var) for edge in self._edges for var in [edge, edge.source_node, edge.destination_node]
        }
        for edge in self._edges:
            connection_query = self._generate_connection_query(edge, set())
            connection_queries.append(connection_query)

        match_query += ', '.join(connection_queries)
        match_query += f' RETURN {", ".join(match_query_variables)}'
        return match_query
