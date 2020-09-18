import flask_restful
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from routes.graph_route import Graph, GraphCollection, graph_blueprint
from socketio_namespaces.graph_namespace import GraphNamespace


def main():
    app = Flask(__name__)
    api = flask_restful.Api(app)

    api.add_resource(GraphCollection, '/graphs')
    api.add_resource(Graph, '/graphs/<int:project_id>')

    app.register_blueprint(graph_blueprint)
    CORS(app)

    socketio = SocketIO(app, cors_allowed_origins="*")
    socketio.on_namespace(GraphNamespace())

    socketio.run(app, debug=True)


if __name__ == '__main__':
    main()
