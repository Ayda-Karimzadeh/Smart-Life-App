"""Demo data seeder for first-time user experience."""

from datetime import date, timedelta

from database.repository import (
    habit_repo,
    goal_repo,
    task_repo,
    time_repo,
)
from core.language_manager import tr
from core.dates import start_of_week


def seed_demo_data():
    """Seed realistic demo data for a better first-time experience.

    Demo data is stored using stable English keys/values.
    User-facing text is translated through tr().
    """

    today = date.today()

    # ==========================================================
    # Demo Habits
    # ==========================================================

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

    for (
        icon,
        name_key,
        category,
        freq_type,
        freq_count,
        pattern,
    ) in demo_habits:

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
        for offset, done in zip(
            range(6, -1, -1),
            pattern,
        ):
            if done:
                log_date = (
                    today - timedelta(days=offset)
                ).isoformat()

                habit_repo.log_habit_on_date(
                    habit_id,
                    log_date,
                )

    # ==========================================================
    # Demo Goals
    # ==========================================================

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

    for (
        icon,
        name_key,
        category,
        days,
        milestone_keys,
    ) in demo_goals:

        name = tr(name_key)

        description = tr(
            "demo_goal_description"
        ).format(name=name)

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

    # ==========================================================
    # Demo Tasks
    # ==========================================================

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

    # ==========================================================
    # Demo Focus Sessions
    # ==========================================================
    #
    # Purpose:
    # Create realistic Focus Time data across the current week
    # so the Dashboard weekly bar chart (get_weekly_activity)
    # has meaningful, varied data.
    #
    # IMPORTANT — why offsets are relative to start_of_week():
    # get_weekly_activity() in db_manager.py builds the chart by
    # iterating week_start .. week_start+6 (Saturday -> Friday).
    # The old version of this seeder computed session dates as
    # `today - timedelta(days=days_ago)`, which silently assumed
    # "today" is always Friday (days_ago=0). Any other day of the
    # week broke the assumption: the generated dates could land
    # outside the current week entirely, so get_weekly_activity()
    # wouldn't find them and the chart looked flat/empty.
    #
    # Fix: compute each session's date from the real start of the
    # current week (index 0 = Saturday ... index 6 = Friday), and
    # only seed days that have already happened (offset <= today's
    # position in the week). Seeding a "future" day inside the
    # current week isn't realistic (you can't log a focus session
    # that hasn't happened yet), and it would misleadingly show a
    # completed bar for a day that hasn't occurred.
    #
    # Target pattern (once the week has fully elapsed):
    #
    # Saturday  -> 1h 20m
    # Sunday    -> 2h 10m
    # Monday    -> 0h 45m
    # Tuesday   -> 2h 35m
    # Wednesday -> 1h 40m
    # Thursday  -> 0h
    # Friday    -> 1h 15m
    #
    # These values are intentionally different so the chart
    # looks like real usage rather than a flat demo. Whatever
    # portion of the week has already passed gets seeded; the
    # rest stays at 0h, which is expected/realistic.
    # ==========================================================

    week_start = start_of_week()

    weekly_focus_sessions = [
        # Saturday (offset 0)
        (
            0,
            [
                ("session_python_study", "Study", 45 * 60),
                ("session_reading", "Study", 35 * 60),
            ],
        ),

        # Sunday (offset 1)
        (
            1,
            [
                ("session_deep_work", "Work", 50 * 60),
                ("session_python_project", "Study", 45 * 60),
                ("session_learning", "Study", 35 * 60),
            ],
        ),

        # Monday (offset 2)
        (
            2,
            [
                ("session_python_study", "Study", 45 * 60),
            ],
        ),

        # Tuesday (offset 3)
        (
            3,
            [
                ("session_deep_work", "Work", 60 * 60),
                ("session_python_project", "Study", 50 * 60),
                ("session_reading", "Study", 45 * 60),
            ],
        ),

        # Wednesday (offset 4)
        (
            4,
            [
                ("session_deep_work", "Work", 50 * 60),
                ("session_learning", "Study", 50 * 60),
            ],
        ),

        # Thursday (offset 5)
        (
            5,
            [],
        ),

        # Friday (offset 6)
        (
            6,
            [
                ("session_week_review", "Study", 45 * 60),
                ("session_planning", "Personal", 30 * 60),
            ],
        ),
    ]

    for offset, sessions in weekly_focus_sessions:

        session_date_obj = week_start + timedelta(days=offset)

        # Never seed a day that's still in the future within the
        # current week — that's not realistic and would corrupt
        # the "real usage" look of the chart.
        if session_date_obj > today:
            continue

        session_date = session_date_obj.isoformat()

        for (
            name_key,
            category,
            duration,
        ) in sessions:

            time_repo.add_time_session(
                tr(name_key),
                category,
                duration,
                session_date=session_date,
            )


def clear_demo_data():
    """Clear all demo data."""

    # ----------------------------------------------------------
    # Habits
    # ----------------------------------------------------------

    habits = habit_repo.get_all_habits()

    for habit in habits:
        habit_repo.delete_habit(habit.id)

    # ----------------------------------------------------------
    # Goals
    # ----------------------------------------------------------

    goals = goal_repo.get_all_goals()

    for goal in goals:
        goal_repo.delete_goal(goal.id)

    # ----------------------------------------------------------
    # Tasks
    # ----------------------------------------------------------

    tasks = task_repo.get_all_tasks()

    for task in tasks:
        task_repo.delete_task(task.id)

    # ----------------------------------------------------------
    # Time Sessions
    # ----------------------------------------------------------

    sessions = time_repo.get_recent_sessions(
        limit=100000
    )

    for session in sessions:
        time_repo.delete_time_session(session.id)