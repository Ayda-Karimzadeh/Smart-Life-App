import unittest
from unittest.mock import patch

from database.demo_data import seed_demo_data


class DemoDataTests(unittest.TestCase):
    @patch("database.demo_data.time_repo")
    @patch("database.demo_data.task_repo")
    @patch("database.demo_data.goal_repo")
    @patch("database.demo_data.habit_repo")
    @patch("database.demo_data.tr", side_effect=lambda key: key)
    def test_seeder_stores_translation_keys_for_localized_entities(
        self, translate, habit_repo, goal_repo, task_repo, time_repo
    ):
        seed_demo_data()

        habit_names = [call.args[0] for call in habit_repo.add_habit.call_args_list]
        self.assertIn("habit_meditation", habit_names)
        self.assertIn("habit_water", habit_names)

        goal_names = [call.args[0] for call in goal_repo.add_goal.call_args_list]
        self.assertIn("goal_learn_something", goal_names)

        milestone_names = [
            call.args[1] for call in goal_repo.add_milestone.call_args_list
        ]
        self.assertIn("ms_choose_topic", milestone_names)


if __name__ == "__main__":
    unittest.main()