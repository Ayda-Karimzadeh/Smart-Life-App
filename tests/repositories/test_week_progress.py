import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from core.dates import end_of_week, start_of_week
from database import db_manager
from database.repository import habit_repo


class WeekProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_manager.DB_PATH
        db_manager.DB_PATH = Path(self.temp_dir.name) / "smart_life_test.db"
        db_manager.init_db()

    def tearDown(self):
        db_manager.DB_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_future_logs_are_excluded_from_week_progress(self):
        habit_id = habit_repo.add_habit("Habit", "*", "Test")
        habit_repo.log_habit_on_date(habit_id, start_of_week().isoformat())
        habit_repo.log_habit_on_date(
            habit_id, (end_of_week() + timedelta(days=1)).isoformat()
        )

        self.assertEqual(habit_repo.get_week_progress(habit_id), 1)


if __name__ == "__main__":
    unittest.main()
