#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, Iterable, List

import neo4j


@dataclass
class Node:
    id: str  # MAC
    labels: List[str]
    properties: Dict[str, str]

    def __init__(self, neo4j_node: neo4j.data.Node):
        self.id = neo4j_node.id
        self.labels = list(set(neo4j_node.labels))
        self.properties = dict(neo4j_node._properties)


@dataclass
class Edge:
    labels: List[str]
    source_node: Node
    destination_node: Node

    def __init__(self, labels: Iterable[str], source_node: Node, destination_node: Node):
        self.labels = list(set(labels))
        self.source_node = source_node
        self.destination_node = destination_node


def generate_creation_query(edges: Iterable[Edge]) -> str:
    creation_query = f'CREATE '
    creation_query_variables = set()
    for edge in edges:
        creation_query_variables.add(variable_name(edge))
        for node in [edge.source_node, edge.destination_node]:
            creation_query += f'({variable_name(node)}'
            if variable_name(node) not in creation_query_variables:
                creation_query_variables.add(variable_name(node))
                properties_dict = node.properties
                properties_dict.update({'id': node.id})
                creation_query += _generate_labels_and_properties_query(node.labels, properties_dict)
            creation_query += ')'

            if node.id == edge.source_node.id:
                creation_query += f'-[{variable_name(edge)}:{":".join(edge.labels)}]->'

        creation_query += ', '

    creation_query = creation_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
    creation_query += f' RETURN {", ".join(creation_query_variables)}'
    return creation_query


def _generate_labels_and_properties_query(labels: Iterable[str], properties: Dict[str, str]) -> str:
    labels_and_properties = f':{":".join(labels)}'
    if len(properties) > 0:
        labels_and_properties += _generate_properties_query(properties)
    return labels_and_properties


def _generate_properties_query(labels_dict: Dict[str, str]) -> str:
    labels_query = ' {'
    for label, value in labels_dict.items():
        labels_query += f"{label}:\'{value}\', "
    labels_query = labels_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
    labels_query += '}'
    return labels_query


def variable_name(obj: any) -> str:
    return 'id_' + str(id(obj))


def generate_match_query(edges: Iterable[Edge]) -> str:
    match_query = 'MATCH '
    connections = []
    match_query_variables = set()
    for edge in edges:
        connection = f'({variable_name(edge.source_node)}{_generate_labels_and_properties_query(edge.source_node.labels, edge.source_node.properties)})'
        connection += f'-[{variable_name(edge)}:{":".join(edge.labels)}]-'
        connection += f'({variable_name(edge.destination_node)}{_generate_labels_and_properties_query(edge.destination_node.labels, edge.destination_node.properties)})'
        connections.append(connection)
        match_query_variables |= {
            variable_name(edge), variable_name(edge.source_node), variable_name(edge.destination_node)
        }
    match_query += ', '.join(connections)
    match_query += f' RETURN {", ".join(match_query_variables)}'
    return match_query


if __name__ == '__main__':
    node1 = Node(neo4j.data.Node(None, n_id='1', n_labels={'Person'}, properties=dict()))
    node2 = Node(
        neo4j.data.Node(
            None, n_id='2', n_labels={'Person', 'Swedish'}, properties={'name': 'Andy', 'title': 'Developer'}
        )
    )
    node3 = Node(neo4j.data.Node(None, n_id='3', n_labels={'Person', 'Murderer'}, properties=dict()))
    this_edges = [Edge({'FRIENDS'}, node1, node2), Edge({'ENEMIES'}, node1, node3)]
    print(generate_creation_query(this_edges))
    print('===============MATCH:=================')
    print(generate_match_query(this_edges))
