from enum import Enum


class GraphEvents(Enum):
    JOINED_ROOM = 'joined_room'
    LEFT_ROOM = 'left_room'
    ADDED = 'added'
    UPDATED = 'updated'
    DELETED = 'deleted'
