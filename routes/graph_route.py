import json
from typing import Dict, List

from flask import Blueprint, jsonify, request
from flask_restful import Resource

from controllers.graph_controller import GraphController
from data_access_layer.consts import DB_FILE_PATH
from models.edge_model import EdgeModel

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
        edges = [EdgeModel(**edge) for edge in data['edges']]

        graph_controller = GraphController(DB_FILE_PATH)
        result = {
            'message': 'Created new graph',
            'status': 'ok',
            'graph': graph_controller.add_graph(project_name, edges)
        }
        return jsonify(result)

    @staticmethod
    def get() -> Dict[str, any]:
        """
        Returns the graphs that match the searched graph
        :return: The matching graphs.
        """
        graph_controller = GraphController(DB_FILE_PATH)
        edges: List[EdgeModel] = [EdgeModel(**edge) for edge in json.loads(request.args.get('edges'))]
        result = {
            'message': 'Fetched graphs successfully',
            'status': 'ok',
            'graphList': graph_controller.get_matching_graphs(edges)
        }
        return jsonify(result)


@graph_blueprint.route('/<int:project_id>')
class Graph(Resource):
    @staticmethod
    def put(project_id: int):
        """
        Updates the project's graph
        :param project_id: The project ID
        :return: The updated project's graph
        """
        data = request.json
        edges = [EdgeModel(**edge) for edge in data['edges']]

        graph_controller = GraphController(DB_FILE_PATH)
        project_name = graph_controller.get_project_name(project_id)
        result = {
            'message': f'Updated graph of project {project_name}',
            'status': 'ok',
            'graph': graph_controller.update_graph(project_name, edges)
        }
        return jsonify(result)

    @staticmethod
    def get(project_id: int):
        """
        Gets the project's graph
        :param project_id: ID
        :return: The project's graph
        """
        graph_controller = GraphController(DB_FILE_PATH)
        project_name = graph_controller.get_project_name(project_id)
        result = {
            'message': f'Fetched graph {project_name} successfully',
            'status': 'ok',
            'graph': graph_controller.get_graph(project_name)
        }
        return jsonify(result)
