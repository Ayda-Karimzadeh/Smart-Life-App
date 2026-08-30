import unittest
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from core.analytics import (
    consistency_score,
    productivity_score,
    strengths_and_weaknesses,
    get_key_insight,
    weekly_report,
)


class ProductivityScoreTests(unittest.TestCase):
    @patch("core.analytics._focus_on", return_value=0)
    @patch("core.analytics.task_repo")
    @patch("core.analytics.habit_repo")
    @patch("core.analytics.get_weekday_labels_short", return_value=["S"] * 7)
    def test_weekly_report_returns_seven_empty_days(
        self, labels, habit_repo, task_repo, focus_on
    ):
        habit_repo.get_all_habits.return_value = []
        task_repo.get_all_tasks.return_value = []

        result = weekly_report()

        self.assertEqual(result["habit_scores"], [0] * 7)
        self.assertEqual(result["focus_hours"], [0] * 7)
        self.assertEqual(result["tasks_done"], [0] * 7)
        self.assertEqual(result["avg_habit_pct"], 0)

    @patch("core.analytics.habit_repo")
    def test_consistency_score_starts_at_habit_creation(self, habit_repo):
        today = date(2026, 8, 25)
        habit_repo.get_all_habits.return_value = [SimpleNamespace(
            id=1,
            frequency_type="daily",
            frequency_count=1,
            created_at="2026-08-24",
        )]
        habit_repo.get_habit_log_count.return_value = 1

        with patch("core.analytics.date", wraps=date) as date_type:
            date_type.today.return_value = today
            result = consistency_score(1, days=30)

        self.assertEqual(result, 50.0)
        habit_repo.get_habit_log_count.assert_called_once_with(
            1, "2026-08-24", "2026-08-25"
        )

    @patch("core.analytics.habit_repo")
    def test_weekly_consistency_uses_only_days_after_habit_creation(self, habit_repo):
        today = date(2026, 8, 25)
        habit_repo.get_all_habits.return_value = [SimpleNamespace(
            id=1,
            frequency_type="weekly",
            frequency_count=3,
            created_at="2026-08-21",
        )]
        habit_repo.get_habit_log_count.return_value = 2

        with patch("core.analytics.date", wraps=date) as date_type:
            date_type.today.return_value = today
            result = consistency_score(1, days=7)

        self.assertEqual(result, 50.0)

    @patch("core.analytics.analytics_repo")
    @patch("core.analytics.task_repo")
    @patch("core.analytics.goal_repo")
    @patch("core.analytics.habit_repo")
    def test_productivity_score_combines_all_weighted_areas(
        self, habit_repo, goal_repo, task_repo, analytics_repo
    ):
        today = date.today().isoformat()
        habit_repo.get_all_habits.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        habit_repo.is_habit_done_today.side_effect = [True, False]
        goal_repo.get_all_goals.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        goal_repo.get_goal_progress_percent.side_effect = [100, 50]
        task_repo.get_all_tasks.return_value = [
            SimpleNamespace(done=True, due_date=today),
            SimpleNamespace(done=True, due_date=today),
            SimpleNamespace(done=False, due_date=today),
            SimpleNamespace(done=False, due_date=today),
        ]
        analytics_repo.get_total_time_today.return_value = 2 * 60 * 60

        self.assertEqual(productivity_score(target_focus_hours=4), 58)

    @patch("core.analytics.analytics_repo")
    @patch("core.analytics.task_repo")
    @patch("core.analytics.goal_repo")
    @patch("core.analytics.habit_repo")
    def test_productivity_score_counts_only_relevant_today_tasks(
        self, habit_repo, goal_repo, task_repo, analytics_repo
    ):
        today = date.today()
        habit_repo.get_all_habits.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        habit_repo.is_habit_done_today.side_effect = [True, False]
        goal_repo.get_all_goals.return_value = [SimpleNamespace(id=1)]
        goal_repo.get_goal_progress_percent.return_value = 100
        task_repo.get_all_tasks.return_value = [
            SimpleNamespace(done=True, due_date=(today - timedelta(days=1)).isoformat()),
            SimpleNamespace(done=False, due_date=today.isoformat()),
        ]
        analytics_repo.get_total_time_today.return_value = 0

        self.assertEqual(productivity_score(target_focus_hours=4), 50)

    @patch("core.analytics.habit_repo")
    def test_strengths_and_weaknesses_return_weaknesses_in_ascending_order(self, habit_repo):
        habit_repo.get_all_habits.return_value = [
            SimpleNamespace(id=1, name="Habit A", icon="A", frequency_type="daily", frequency_count=1),
            SimpleNamespace(id=2, name="Habit B", icon="B", frequency_type="daily", frequency_count=1),
            SimpleNamespace(id=3, name="Habit C", icon="C", frequency_type="daily", frequency_count=1),
            SimpleNamespace(id=4, name="Habit D", icon="D", frequency_type="daily", frequency_count=1),
        ]

        with patch("core.analytics.consistency_score", side_effect=[90, 30, 20, 10]):
            result = strengths_and_weaknesses()

        self.assertEqual([item["name"] for item in result["strengths"]], ["Habit A", "Habit B", "Habit C"])
        self.assertEqual([item["name"] for item in result["weaknesses"]], ["Habit D", "Habit C", "Habit B"])

    @patch("core.analytics.tr")
    @patch("core.analytics.habit_repo")
    @patch("core.analytics.goal_repo")
    @patch("core.analytics.daily_streak")
    def test_get_key_insight_uses_daily_streak_engine(self, daily_streak, goal_repo, habit_repo, tr_mock):
        habit_repo.get_all_habits.return_value = [SimpleNamespace(id=1, name="Workout")]
        goal_repo.get_all_goals.return_value = []
        daily_streak.return_value = 5
        tr_mock.side_effect = lambda key, *args, **kwargs: key if key != "insight_streak" else "{habit} has {streak} day streak"

        result = get_key_insight()

        self.assertIsNotNone(result)
        self.assertEqual(result["value"], 5)
        self.assertIn("Workout", result["message"])


if __name__ == "__main__":
    unittest.main()