import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.connection  = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()

if __name__ == "__main__":
    db = Database()
    print("Database Created Successfully")