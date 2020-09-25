import json
from typing import Dict

from flask import Blueprint, jsonify, request
from flask_restful import Resource

from controllers.graph_controller import GraphController
from models.edge_model import EdgeModel
from models.graph_update_request_model import GraphUpdateRequestModel
from models.node_model import NodeModel
from models.relationship_model import RelationshipModel

graph_blueprint = Blueprint('graphs', __name__)


@graph_blueprint.route('/')
class GraphCollection(Resource):
    @staticmethod
    def post() -> Dict[str, any]:
        """
        Adds a new graph to the graph collection
        :return: The updated graph collection
        """
        data = request.json
        project_name = data['project_name']
        edges = [EdgeModel(edge_dict) for edge_dict in data['edges']]
        nodes = [NodeModel.from_dict(node_dict) for node_dict in data['nodes']]

        graph_controller = GraphController()
        result = {
            'message': 'Created new graph',
            'status': 'ok',
            'graph': graph_controller.add_graph(project_name, edges, nodes)
        }
        return jsonify(result)

    @staticmethod
    def get() -> Dict[str, any]:
        """
        Returns the graphs that match the searched graph
        :return: The matching graphs.
        """
        graph_controller = GraphController()
        edges = [EdgeModel(edge_dict) for edge_dict in json.loads(request.args.get('edges'))]
        result = {
            'message': 'Fetched graphs successfully',
            'status': 'ok',
            'graphList': graph_controller.get_matching_graphs(edges)
        }
        return jsonify(result)


@graph_blueprint.route('/<string:project_name>')
class Graph(Resource):
    @staticmethod
    def put(project_name: str):
        """
        Updates the project's graph
        :param project_name: The project name
        :return: The updated project's graph
        """
        data = request.json
        graph_update_request_model = Graph._get_graph_update_request_model(data)
        graph_controller = GraphController()
        result = {
            'message': f'Updated graph of project {project_name}',
            'status': 'ok',
            'graph': graph_controller.update_graph(project_name, graph_update_request_model)
        }
        return jsonify(result)

    @staticmethod
    def _get_graph_update_request_model(data: Dict[str, any]):
        nodes_to_add = [NodeModel(node_dict) for node_dict in data['nodes']['add']]
        nodes_to_update = [NodeModel(node_dict) for node_dict in data['nodes']['update']]
        nodes_to_delete = [NodeModel(node_dict) for node_dict in data['nodes']['delete']]
        relationships_to_add = [
            RelationshipModel(relationship_dict) for relationship_dict in data['relationship_dict']['add']
        ]
        relationships_to_update = [
            RelationshipModel(relationship_dict) for relationship_dict in data['relationship_dict']['update']
        ]
        relationships_to_delete = [
            RelationshipModel(relationship_dict) for relationship_dict in data['relationship_dict']['delete']
        ]
        return GraphUpdateRequestModel(
            nodes_to_add, nodes_to_update, nodes_to_delete,
            relationships_to_add, relationships_to_update, relationships_to_delete
        )

    @staticmethod
    def get(project_name: str):
        """
        Gets the project's graph
        :param project_name: The project name
        :return: The project's graph
        """
        graph_controller = GraphController()
        result = {
            'message': f'Fetched graph {project_name} successfully',
            'status': 'ok',
            'graph': graph_controller.get_graph(project_name)
        }
        return jsonify(result)
