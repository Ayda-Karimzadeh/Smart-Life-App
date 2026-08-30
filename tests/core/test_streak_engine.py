import unittest
from datetime import date, timedelta
from unittest.mock import patch

from core.dates import start_of_week
from core.streak_engine import (
    best_daily_streak,
    best_weekly_streak,
    daily_streak,
    week_status,
    weekly_streak,
)


class StreakEngineTests(unittest.TestCase):
    @patch("core.streak_engine.habit_repo")
    def test_daily_streak_is_zero_without_logs(self, habit_repo):
        habit_repo.get_habit_log_dates.return_value = []

        self.assertEqual(daily_streak(1), 0)

    @patch("core.streak_engine.habit_repo")
    def test_best_daily_streak_returns_longest_run(self, habit_repo):
        habit_repo.get_habit_log_dates.return_value = [
            "2026-08-20",
            "2026-08-21",
            "2026-08-23",
            "2026-08-24",
            "2026-08-25",
        ]

        self.assertEqual(best_daily_streak(1), 3)

    @patch("core.streak_engine.habit_repo")
    def test_daily_streak_counts_consecutive_logs_through_today(self, habit_repo):
        today = date(2026, 8, 24)
        habit_repo.get_habit_log_dates.return_value = [
            (today - timedelta(days=offset)).isoformat() for offset in range(3)
        ]

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            self.assertEqual(daily_streak(1), 3)

        habit_repo.get_habit_log_dates.assert_called_once_with(1, order="DESC")

    @patch("core.streak_engine.habit_repo")
    def test_daily_streak_is_zero_when_today_is_missing(self, habit_repo):
        today = date(2026, 8, 24)
        habit_repo.get_habit_log_dates.return_value = [
            (today - timedelta(days=1)).isoformat(),
            (today - timedelta(days=2)).isoformat(),
        ]

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            self.assertEqual(daily_streak(1), 0)

    @patch("core.streak_engine.habit_repo")
    def test_weekly_streak_counts_consecutive_completed_weeks(self, habit_repo):
        today = date(2026, 8, 24)
        current_week = start_of_week(today)
        previous_week = current_week - timedelta(weeks=1)
        ranges = {
            (current_week.isoformat(), today.isoformat()): 3,
            (
                previous_week.isoformat(),
                (previous_week + timedelta(days=6)).isoformat(),
            ): 3,
        }
        habit_repo.get_habit_frequency_count.return_value = 3
        habit_repo.count_logs_in_range.side_effect = (
            lambda _habit_id, start, end: ranges.get((start, end), 0)
        )

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            self.assertEqual(weekly_streak(1), 2)

    @patch("core.streak_engine.habit_repo")
    def test_best_weekly_streak_ignores_incomplete_current_week(self, habit_repo):
        today = date(2026, 8, 24)
        current_week = start_of_week(today)
        previous_week = current_week - timedelta(weeks=1)
        ranges = {
            (current_week.isoformat(), today.isoformat()): 2,
            (
                previous_week.isoformat(),
                (previous_week + timedelta(days=6)).isoformat(),
            ): 3,
        }
        habit_repo.get_habit_created_at.return_value = "2026-08-10"
        habit_repo.get_habit_frequency_count.return_value = 3
        habit_repo.count_logs_in_range.side_effect = (
            lambda _habit_id, start, end: ranges.get((start, end), 0)
        )

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            self.assertEqual(best_weekly_streak(1), 1)

    @patch("core.streak_engine.habit_repo")
    def test_week_status_caps_target_for_new_habit(self, habit_repo):
        today = date(2026, 8, 25)
        habit_repo.get_habit_frequency_count.return_value = 7
        habit_repo.get_habit_created_at.return_value = "2026-08-24"
        habit_repo.count_logs_in_range.return_value = 1
        habit_repo.get_habit_log_dates.return_value = []

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            result = week_status(1)

        self.assertEqual(result["effective_target"], 5)
        self.assertEqual(result["done"], 1)
        self.assertEqual(result["pct"], 20)

    @patch("core.streak_engine.habit_repo")
    def test_week_status_marks_unreachable_target_broken(self, habit_repo):
        today = date(2026, 8, 25)
        habit_repo.get_habit_frequency_count.return_value = 7
        habit_repo.get_habit_created_at.return_value = "2026-08-22"
        habit_repo.count_logs_in_range.return_value = 0
        habit_repo.get_habit_log_dates.return_value = []

        with patch("core.streak_engine.date") as date_type:
            date_type.today.return_value = today
            result = week_status(1)

        self.assertEqual(result["status"], "broken")


if __name__ == "__main__":
    unittest.main()