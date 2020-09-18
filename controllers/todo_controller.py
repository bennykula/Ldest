import sqlite3
from typing import List

from controllers.todo_controller_exceptions import EmptyTitleError, NoSuchRoomError
from models.todo_model import TodoModel
from utils.singleton import Singleton


class TodoController(metaclass=Singleton):
    def __init__(self, db_path) -> None:
        self._db_path = db_path

    def create_new_todo(self, room: str, todo: TodoModel) -> TodoModel:
        if todo.title.strip() == '':
            raise EmptyTitleError()

        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        new_id = self._get_last_id(room) + 1
        cursor.execute(f"INSERT INTO todos VALUES ({todo.userId}, {new_id}, '{todo.title}', '{room}')")
        connection.commit()
        connection.close()

        result = todo
        result.id = new_id
        return result

    def _get_last_id(self, room: str) -> int:
        connection = sqlite3.connect(self._db_path)
        curosr = connection.cursor()
        for row in curosr.execute(f"SELECT MAX(id) FROM todos WHERE room='{room}'"):
            last_id, = row
            connection.close()
            return last_id

    def get_all_todos(self, room: str) -> List[TodoModel]:
        result = []
        if not self._is_room_exists(room):
            raise NoSuchRoomError()

        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        for row in cursor.execute(f"SELECT * FROM todos WHERE room='{room}'"):
            result.append(TodoModel(row[0], row[1], row[2]))
        connection.close()
        return result

    def _is_room_exists(self, room: str) -> bool:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM todos WHERE room='{room}'")

        result = cursor.fetchone()
        connection.close()
        return result is not None

    def delete_todo(self, todo_id: int) -> int:
        sql = f'DELETE FROM todos WHERE id={todo_id}'
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return todo_id

    def update_todo(self, todo: TodoModel) -> TodoModel:
        if todo.title.strip() == '':
            raise EmptyTitleError()
        sql = f" UPDATE todos SET userId = {todo.userId}, title = '{todo.title}' WHERE id = {todo.id}"
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return todo
