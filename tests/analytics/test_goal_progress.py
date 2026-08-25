import unittest
import tempfile
from pathlib import Path

from database import db_manager
from database.repository import goal_repo


class GoalProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_manager.DB_PATH
        db_manager.DB_PATH = Path(self.temp_dir.name) / "smart_life_test.db"
        db_manager.init_db()

    def tearDown(self):
        db_manager.DB_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_goal_progress_is_percentage_of_completed_milestones(self):
        goal_id = goal_repo.add_goal("Goal", "", "*", "Test", None)
        goal_repo.add_milestone(goal_id, "First")
        goal_repo.add_milestone(goal_id, "Second")
        goal_repo.add_milestone(goal_id, "Third")
        goal_repo.toggle_milestone(goal_repo.get_milestones(goal_id)[0].id)

        self.assertEqual(goal_repo.get_goal_progress_percent(goal_id), 33)

    def test_goal_without_milestones_has_zero_progress(self):
        goal_id = goal_repo.add_goal("Goal", "", "*", "Test", None)

        self.assertEqual(goal_repo.get_goal_progress_percent(goal_id), 0)


if __name__ == "__main__":
    unittest.main()