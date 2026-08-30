import tempfile
import unittest
from datetime import date
from pathlib import Path

from database import db_manager
from database.repository import settings_repo, task_repo, time_repo


class CrudAndSettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_manager.DB_PATH
        db_manager.DB_PATH = Path(self.temp_dir.name) / "smart_life_test.db"
        db_manager.init_db()

    def tearDown(self):
        db_manager.DB_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_task_crud_and_toggle(self):
        task_repo.add_task("Task", "Description", "Work", "High", date.today().isoformat())
        task = task_repo.get_all_tasks()[0]

        task_repo.update_task(task.id, "Updated", "Changed", "Personal", "Low")
        updated = task_repo.get_all_tasks()[0]
        self.assertEqual((updated.name, updated.description, updated.category),
                         ("Updated", "Changed", "Personal"))

        task_repo.toggle_task(task.id)
        self.assertTrue(task_repo.get_all_tasks()[0].done)
        task_repo.delete_task(task.id)
        self.assertEqual(task_repo.get_all_tasks(), [])

    def test_task_done_filter(self):
        task_repo.add_task("Pending", "", "Work", "Low")
        task_repo.add_task("Done", "", "Work", "Low")
        done_task = task_repo.get_all_tasks()[1]
        task_repo.toggle_task(done_task.id)

        self.assertEqual([task.name for task in task_repo.get_all_tasks(done=True)], ["Done"])
        self.assertEqual([task.name for task in task_repo.get_all_tasks(done=False)], ["Pending"])

    def test_time_session_crud_and_totals(self):
        time_repo.add_time_session("Focus", "Study", 1800)
        session = time_repo.get_sessions_today()[0]
        self.assertEqual(time_repo.get_total_time_today(), 1800)

        time_repo.update_time_session(session.id, "Deep Focus", "Work", 3600)
        self.assertEqual(time_repo.get_total_time_today(), 3600)
        self.assertEqual(time_repo.get_sessions_today()[0].name, "Deep Focus")

        time_repo.delete_time_session(session.id)
        self.assertEqual(time_repo.get_sessions_today(), [])

    def test_settings_round_trip(self):
        self.assertEqual(settings_repo.get("missing", "fallback"), "fallback")
        settings_repo.set("theme", "dark")
        self.assertEqual(settings_repo.get("theme"), "dark")
        settings_repo.set_user_name("Sara")
        self.assertEqual(settings_repo.get_user_name(), "Sara")
        self.assertFalse(settings_repo.is_onboarding_completed())
        settings_repo.mark_onboarding_completed()
        self.assertTrue(settings_repo.is_onboarding_completed())


if __name__ == "__main__":
    unittest.main()
