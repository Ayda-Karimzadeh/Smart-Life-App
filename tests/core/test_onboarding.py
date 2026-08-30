import unittest
from unittest.mock import patch

from ui.onboarding import should_show_onboarding


class OnboardingStateTests(unittest.TestCase):
    @patch("ui.onboarding.goal_repo")
    @patch("ui.onboarding.habit_repo")
    @patch("ui.onboarding.settings_repo")
    def test_completed_state_skips_onboarding_without_reading_data(
        self, settings_repo, habit_repo, goal_repo
    ):
        settings_repo.is_onboarding_completed.return_value = True

        self.assertFalse(should_show_onboarding())
        habit_repo.get_all_habits.assert_not_called()
        goal_repo.get_all_goals.assert_not_called()

    @patch("ui.onboarding.goal_repo")
    @patch("ui.onboarding.habit_repo")
    @patch("ui.onboarding.settings_repo")
    def test_existing_data_marks_onboarding_completed(
        self, settings_repo, habit_repo, goal_repo
    ):
        settings_repo.is_onboarding_completed.return_value = False
        habit_repo.get_all_habits.return_value = [object()]
        goal_repo.get_all_goals.return_value = []

        self.assertFalse(should_show_onboarding())
        settings_repo.mark_onboarding_completed.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
