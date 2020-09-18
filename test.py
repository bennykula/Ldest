#!/usr/bin/env python3

import neo4j

from data_access_layer.neo4j_database.neo4j_queries_generator import Neo4jQueriesGenerator
from models.edge_model import EdgeModel
from models.node_model import NodeModel

if __name__ == '__main__':
    node1 = NodeModel(neo4j.data.Node(None, n_id='1', n_labels={'Person'}, properties=dict()))
    node2 = NodeModel(
        neo4j.data.Node(
            None, n_id='2', n_labels={'Person', 'Swedish'}, properties={'name': 'Andy', 'title': 'Developer'}
        )
    )
    node3 = NodeModel(neo4j.data.Node(None, n_id='3', n_labels={'Person', 'Murderer'}, properties=dict()))
    this_edges = [EdgeModel({'FRIENDS'}, node1, node2), EdgeModel({'ENEMIES'}, node1, node3)]
    print(Neo4jQueriesGenerator(this_edges).generate_creation_query())
    print('===============MATCH:=================')
    print(Neo4jQueriesGenerator(this_edges).generate_match_query())
