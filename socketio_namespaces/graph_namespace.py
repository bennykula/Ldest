from typing import Dict

from flask_socketio import Namespace, emit, join_room, leave_room

from socketio_namespaces.graph_events import GraphEvents


class GraphNamespace(Namespace):
    def __init__(self) -> None:
        super().__init__()
        self.namespace = '/todo'

    def on_joined_room(self, room: str) -> None:
        join_room(room, namespace=self.namespace)
        emit(GraphEvents.JOINED_ROOM.value, f'Joined room: {room}', namespace=self.namespace)

    def on_left_room(self, room: str) -> None:
        leave_room(room)
        emit(GraphEvents.LEFT_ROOM.value, f'Left room: {room}', namespace=self.namespace)

    def on_added(self, added_graph_response: Dict[str, any]) -> None:
        emit(GraphEvents.ADDED.value, added_graph_response['graph'], namespace=self.namespace,
             room=added_graph_response['room'], include_self=False)

    def on_updated(self, updated_graph_response: Dict[str, any]) -> None:
        emit(GraphEvents.UPDATED.value, updated_graph_response['graph'], namespace=self.namespace,
             room=updated_graph_response['room'], include_self=False)

    def on_deleted(self, deleted_graph_response: Dict[str, any]) -> None:
        emit(GraphEvents.DELETED.value, deleted_graph_response['project_name'], namespace=self.namespace,
             room=deleted_graph_response['room'], include_self=False)
