"""Demo data seeder for first-time user experience."""

from datetime import date, timedelta

from database.repository import habit_repo, goal_repo, task_repo, time_repo
from core.language_manager import tr


def seed_demo_data():
    """Seed demo data for a better first-time experience.

    Demo data is stored using stable English keys/values.
    User-facing text is translated through tr().
    """

    today = date.today()

    # ── Demo Habits ──────────────────────────────────────────────────────
    # Stored values remain in English so repository/database logic
    # stays language-independent.
    demo_habits = [
        (
            "🧘",
            "habit_meditation",
            "Mindfulness",
            "daily",
            7,
            [True, True, True, True, True, True, False],
        ),
        (
            "💪",
            "habit_exercise",
            "Fitness",
            "weekly",
            3,
            [True, False, False, True, False, False, True],
        ),
        (
            "📚",
            "habit_reading",
            "Personal Growth",
            "daily",
            7,
            [True, True, False, True, True, False, True],
        ),
        (
            "💧",
            "habit_water",
            "Health",
            "daily",
            8,
            [True, True, True, True, True, True, True],
        ),
        (
            "🌙",
            "habit_sleep",
            "Health",
            "daily",
            7,
            [False, True, False, False, True, False, False],
        ),
        (
            "📓",
            "habit_journal",
            "Mindfulness",
            "daily",
            7,
            [True, False, True, False, False, True, False],
        ),
    ]

    for icon, name_key, category, freq_type, freq_count, pattern in demo_habits:
        name = tr(name_key)

        habit_id = habit_repo.add_habit(
            name,
            icon,
            category,
            freq_type,
            freq_count,
        )

        # pattern[0] = 6 days ago
        # pattern[-1] = today
        for offset, done in zip(range(6, -1, -1), pattern):
            if done:
                log_date = (
                    today - timedelta(days=offset)
                ).isoformat()

                habit_repo.log_habit_on_date(
                    habit_id,
                    log_date,
                )

    # ── Demo Goals ───────────────────────────────────────────────────────
    demo_goals = [
        (
            "🎯",
            "goal_learn_something",
            "Learning",
            90,
            [
                "ms_choose_topic",
                "ms_beginner_lessons",
            ],
        ),
        (
            "💪",
            "goal_get_fit",
            "Fitness",
            180,
            [
                "ms_create_workout_plan",
                "ms_complete_first_month",
            ],
        ),
        (
            "📖",
            "goal_read_books",
            "Personal",
            365,
            [
                "ms_finish_first_book",
            ],
        ),
        (
            "💰",
            "goal_save_money",
            "Finance",
            365,
            [
                "ms_set_saving_target",
            ],
        ),
    ]

    for icon, name_key, category, days, milestone_keys in demo_goals:
        name = tr(name_key)

        description = tr("demo_goal_description").format(
            name=name
        )

        deadline = (
            today + timedelta(days=days)
        ).isoformat()

        goal_id = goal_repo.add_goal(
            name,
            description,
            icon,
            category,
            deadline,
        )

        for milestone_key in milestone_keys:
            goal_repo.add_milestone(
                goal_id,
                tr(milestone_key),
            )

    # ── Demo Tasks ───────────────────────────────────────────────────────
    demo_tasks = [
        (
            "task_finish_python_exercise",
            "task_python_exercise_desc",
            "Learning",
            "High",
            today.isoformat(),
        ),
        (
            "task_go_for_run",
            "task_go_for_run_desc",
            "Fitness",
            "Medium",
            today.isoformat(),
        ),
        (
            "task_reply_emails",
            "task_reply_emails_desc",
            "Work",
            "Low",
            today.isoformat(),
        ),
        (
            "task_book_dentist",
            "task_book_dentist_desc",
            "Personal",
            "Medium",
            (today - timedelta(days=1)).isoformat(),
        ),
        (
            "task_read_chapter",
            "task_read_chapter_desc",
            "Personal",
            "Low",
            (today + timedelta(days=1)).isoformat(),
        ),
        (
            "task_grocery_shopping",
            "task_grocery_shopping_desc",
            "Personal",
            "Medium",
            (today + timedelta(days=2)).isoformat(),
        ),
    ]

    for (
        name_key,
        desc_key,
        category,
        priority,
        due_date,
    ) in demo_tasks:

        task_repo.add_task(
            tr(name_key),
            tr(desc_key),
            category,
            priority,
            due_date,
        )

    # ── Demo Time Sessions ──────────────────────────────────────────────
    # Categories remain stable English database values.
    demo_sessions = [
        ("session_python_study", "Study", 45 * 60),
        ("session_deep_work", "Work", 50 * 60),
        ("session_evening_run", "Fitness", 30 * 60),
        ("session_journaling", "Personal", 15 * 60),
        ("session_book_reading", "Study", 25 * 60),
    ]

    for name_key, category, duration in demo_sessions:
        time_repo.add_time_session(
            tr(name_key),
            category,
            duration,
        )


def clear_demo_data():
    """Clear all demo data."""

    habits = habit_repo.get_all_habits()

    for habit in habits:
        habit_repo.delete_habit(habit.id)

    goals = goal_repo.get_all_goals()

    for goal in goals:
        goal_repo.delete_goal(goal.id)

    tasks = task_repo.get_all_tasks()

    for task in tasks:
        task_repo.delete_task(task.id)

    sessions = time_repo.get_recent_sessions(
        limit=100000
    )

    for session in sessions:
        time_repo.delete_time_session(session.id)