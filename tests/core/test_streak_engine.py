import unittest
from datetime import date, timedelta
from unittest.mock import patch

from core.dates import start_of_week
from core.streak_engine import daily_streak, weekly_streak


class StreakEngineTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()