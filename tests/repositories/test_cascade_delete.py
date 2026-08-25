import tempfile
import unittest
from datetime import date
from pathlib import Path

from database import db_manager
from database.repository import goal_repo, habit_repo


class CascadeDeleteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "smart_life_test.db"
        self.original_database_path = db_manager.DB_PATH
        db_manager.DB_PATH = self.database_path
        db_manager.init_db()

    def tearDown(self):
        db_manager.DB_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_deleting_habit_cascades_to_habit_logs(self):
        habit_id = habit_repo.add_habit("Habit", "*", "Test")
        habit_repo.log_habit_on_date(habit_id, date.today().isoformat())

        habit_repo.delete_habit(habit_id)

        connection = db_manager.get_connection()
        try:
            remaining = connection.execute(
                "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ?", (habit_id,)
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(remaining, 0)

    def test_deleting_goal_cascades_to_milestones(self):
        goal_id = goal_repo.add_goal("Goal", "", "*", "Test", None)
        goal_repo.add_milestone(goal_id, "Milestone")

        goal_repo.delete_goal(goal_id)

        connection = db_manager.get_connection()
        try:
            remaining = connection.execute(
                "SELECT COUNT(*) FROM milestones WHERE goal_id = ?", (goal_id,)
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(remaining, 0)


if __name__ == "__main__":
    unittest.main()