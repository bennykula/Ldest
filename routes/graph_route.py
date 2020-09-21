import json
from typing import Dict

from flask import Blueprint, jsonify, request
from flask_restful import Resource

from controllers.graph_controller import GraphController
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
        edges = [EdgeModel(edge) for edge in data['edges']]

        graph_controller = GraphController()
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
        graph_controller = GraphController()
        edges = [EdgeModel(edge) for edge in json.loads(request.args.get('edges'))]
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
        edges = [EdgeModel(edge) for edge in data['edges']]

        graph_controller = GraphController()
        result = {
            'message': f'Updated graph of project {project_name}',
            'status': 'ok',
            'graph': graph_controller.update_graph(project_name, edges)
        }
        return jsonify(result)

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
