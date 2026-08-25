import unittest
from types import SimpleNamespace
from unittest.mock import patch

from core.analytics import productivity_score


class ProductivityScoreTests(unittest.TestCase):
    @patch("core.analytics.analytics_repo")
    @patch("core.analytics.task_repo")
    @patch("core.analytics.goal_repo")
    @patch("core.analytics.habit_repo")
    def test_productivity_score_combines_all_weighted_areas(
        self, habit_repo, goal_repo, task_repo, analytics_repo
    ):
        habit_repo.get_all_habits.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        habit_repo.is_habit_done_today.side_effect = [True, False]
        goal_repo.get_all_goals.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        goal_repo.get_goal_progress_percent.side_effect = [100, 50]
        task_repo.get_all_tasks.return_value = [
            SimpleNamespace(done=True),
            SimpleNamespace(done=True),
            SimpleNamespace(done=False),
            SimpleNamespace(done=False),
        ]
        analytics_repo.get_total_time_today.return_value = 2 * 60 * 60

        self.assertEqual(productivity_score(target_focus_hours=4), 58)


if __name__ == "__main__":
    unittest.main()