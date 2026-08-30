import unittest
from types import SimpleNamespace
from unittest.mock import patch

from core.habit_feedback import get_habit_toggle_feedback


class HabitFeedbackTests(unittest.TestCase):
    @patch("core.habit_feedback.tr")
    @patch("core.habit_feedback.habit_repo")
    @patch("core.habit_feedback.daily_streak")
    def test_milestone_has_priority_over_perfect_day(self, daily_streak, habit_repo, tr_mock):
        habit_repo.get_all_habits.return_value = [
            SimpleNamespace(id=1),
            SimpleNamespace(id=2),
        ]
        habit_repo.is_habit_done_today.side_effect = [True, True]
        daily_streak.return_value = 3
        tr_mock.side_effect = lambda key, *args, **kwargs: {
            "streak_milestone_title": "{streak}-Day Streak!",
            "streak_milestone_desc": "\"{name}\" for {streak} days in a row!",
            "habit_unchecked": "Marked as undone",
            "habit_unchecked_desc": "\"{name}\" is unchecked for today.",
            "perfect_day": "Perfect Day",
            "perfect_day_desc": "You've completed all your habits today.",
            "habit_completed": "Nice work!",
            "habit_completed_desc": "\"{name}\" is done for today.",
        }.get(key, key)

        title, message, icon, kind = get_habit_toggle_feedback(1, "Workout", False)

        self.assertEqual(title, "3-Day Streak!")
        self.assertEqual(icon, "🔥")
        self.assertEqual(kind, "milestone")
        self.assertIn("Workout", message)

    @patch("core.habit_feedback.tr")
    @patch("core.habit_feedback.habit_repo")
    @patch("core.habit_feedback.daily_streak")
    def test_uses_literal_habit_name_without_translation_lookup(self, daily_streak, habit_repo, tr_mock):
        habit_repo.get_all_habits.return_value = []
        daily_streak.return_value = 1
        tr_mock.side_effect = lambda key, *args, **kwargs: {
            "habit_completed": "Nice work!",
            "habit_completed_desc": "\"{name}\" is done for today.",
        }.get(key, key)

        _, message, _, _ = get_habit_toggle_feedback(1, "My Custom Habit", False)

        self.assertIn("My Custom Habit", message)


if __name__ == "__main__":
    unittest.main()
