from database.database import Database

class TaskRepository:
    def __init__(self):
        self.db = Database()

    def add_task(self, title):
        self.db.cursor.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        self.db.connection.commit()

    def get_all_tasks(self):
        self.db.cursor.execute("SELECT id, title, is_done FROM tasks")
        return self.db.cursor.fetchall()

    def delete_task(self, task_id):
        self.db.cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        self.db.connection.commit()

    def update_task(self, task_id, new_title):
        self.db.cursor.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (new_title, task_id)
        )
        self.db.connection.commit()

    def toggle_task(self, task_id, is_done):
        self.db.cursor.execute(
            "UPDATE tasks SET is_done = ? WHERE id = ?",
            (is_done, task_id)
        )
        self.db.connection.commit()