import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import db_manager


class DatabaseMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_manager.DB_PATH
        db_manager.DB_PATH = Path(self.temp_dir.name) / "smart_life_test.db"

    def tearDown(self):
        db_manager.DB_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_new_database_records_current_schema_version(self):
        db_manager.init_db()

        connection = db_manager.get_connection()
        try:
            version = connection.execute(
                "SELECT version FROM schema_version WHERE id = 1"
            ).fetchone()[0]
        finally:
            connection.close()

        self.assertEqual(version, db_manager.CURRENT_SCHEMA_VERSION)

    def test_existing_database_without_version_is_registered(self):
        connection = sqlite3.connect(db_manager.DB_PATH)
        connection.execute("CREATE TABLE legacy (id INTEGER PRIMARY KEY)")
        connection.commit()
        connection.close()

        db_manager.init_db()

        connection = db_manager.get_connection()
        try:
            version = connection.execute(
                "SELECT version FROM schema_version WHERE id = 1"
            ).fetchone()[0]
            legacy_exists = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'legacy'"
            ).fetchone()
        finally:
            connection.close()

        self.assertEqual(version, db_manager.CURRENT_SCHEMA_VERSION)
        self.assertIsNotNone(legacy_exists)


if __name__ == "__main__":
    unittest.main()