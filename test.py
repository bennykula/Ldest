#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

class Edge: pass

@dataclass
class Node:
    id: str  # MAC
    type: str
    labels: Dict[str, str]

@dataclass
class Edge:
    type: str
    source_node: Node
    destination_node: Node 


# TODO: Add ID
def generate_nodes_creation_query(nodes: List[Node]) -> str:
    nodes_creation_query = f'CREATE'
    for node in nodes:
        nodes_creation_query += f' (:{node.type}'
        labels_dict = node.labels
        labels_dict.update({'id': node.id})
        if len(labels_dict) > 0:
            nodes_creation_query += _generate_labels_query(labels_dict)
        nodes_creation_query += '),'
    nodes_creation_query = nodes_creation_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
    return nodes_creation_query


def _generate_labels_query(labels_dict: Dict[str, str]) -> str:
    labels_query = ' {'
    for label, value in labels_dict.items():
        labels_query += f"{label}:\'{value}\', "
    labels_query = labels_query.rstrip().rstrip(',')  # remove whitespaces and extra ','
    labels_query += '}'
    return labels_query


def generate_edges_creation_query(edges: List[Edge]) -> str:
    edges_creation_query = f''
    for edge in edges:
        edges_creation_query += f'MATCH (source_node), (destination_node)'
        edges_creation_query += f' WHERE source_node.id = \'{edge.source_node_id}\''
        edges_creation_query += f' AND destination_node.id = \'{edge.destination_node_id}\''
        edges_creation_query += f' CREATE (source_node)-[:{edge.type}]->(destination_node)'
        edges_creation_query += '; '
    edges_creation_query.rstrip().rstrip()
    return edges_creation_query

def graph_id(obj):
    return 'id_' + str(id(obj))

def generate_match(edges: List[Edge]) -> str:
    query= 'MATCH '
    connections = []
    for edge in edges:
        connections.append(f'({graph_id(edge.source_node)}) -[{graph_id(edge)}]- ({graph_id(edge.destination_node)})')
    query += ', '.join(connections)
    return query


def add_edge(src:Node, dst:Node, t:str):
    edge = Edge(t, src, dst)

node1 = Node('1', 'Person', dict())
node2 = Node('2', 'Person', {'name': 'Andy', 'title': 'Developer'})
node3 = Node('3', 'Person', dict())
this_nodes = [node1, node2, node3]
# print(generate_nodes_creation_query(this_nodes))
this_edges = [Edge('FRIENDS', node1, node2), Edge('ENEMIES', node1, node3)]
# print(generate_edges_creation_query(this_edges))
print('===============MATCH:=================')
print(generate_match(this_edges))
