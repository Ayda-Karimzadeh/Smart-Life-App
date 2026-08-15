"""Demo data seeder for first-time user experience."""

from datetime import date, timedelta
from database.repository import habit_repo, goal_repo, task_repo, time_repo


def seed_demo_data():
    """Seed demo data for a better first-time experience.

    نکته: مقادیر category دقیقاً با گزینه‌های دراپ‌داون هر بخش
    (AddHabitDialog / AddTaskDialog / AddGoalDialog / EditSessionDialog)
    هم‌خوانی دارن تا از translate_category() درست عبور کنن.
    """

    today = date.today()

    # ── Demo Habits ──────────────────────────────────────────────────────
    # هر عادت یه الگوی تکمیل متفاوت داره تا streak/at_risk/analytics
    # با داده‌ی متنوع‌تری نمایش داده بشه (نه همه چیز 100% یا یکسان).
    demo_habits = [
        # (icon, name, category, freq_type, freq_count, پترن ۷ روز اخیر: True=انجام‌شده)
        ("🧘", "Morning Meditation", "Mindfulness", "daily", 7,
         [True, True, True, True, True, True, False]),   # استریک قوی
        ("💪", "Exercise", "Fitness", "weekly", 3,
         [True, False, False, True, False, False, True]),  # هفتگی، ۳ بار
        ("📚", "Reading", "Personal Growth", "daily", 7,
         [True, True, False, True, True, False, True]),   # خوب ولی نه کامل
        ("💧", "Drink Water", "Health", "daily", 8,
         [True, True, True, True, True, True, True]),     # کامل
        ("🌙", "Sleep Early", "Health", "daily", 7,
         [False, True, False, False, True, False, False]), # در حال افت (at_risk)
        ("📓", "Journaling", "Mindfulness", "daily", 7,
         [True, False, True, False, False, True, False]),  # نامنظم
    ]

    for icon, name, cat, freq_type, freq_count, pattern in demo_habits:
        habit_id = habit_repo.add_habit(name, icon, cat, freq_type, freq_count)
        # pattern[0] مربوط به ۶ روز پیش و pattern[-1] مربوط به امروزه
        for offset, done in zip(range(6, -1, -1), pattern):
            if done:
                log_date = (today - timedelta(days=offset)).isoformat()
                habit_repo.log_habit_on_date(habit_id, log_date)

    # ── Demo Goals ───────────────────────────────────────────────────────
    demo_goals = [
        ("🎯", "Learn Python", "Learning", 90,
         ["Chose a learning path", "Finished beginner lessons"]),
        ("💪", "Get Fit", "Fitness", 180,
         ["Created a workout plan", "Completed first month"]),
        ("📖", "Read 12 Books", "Personal", 365,
         ["Finished book #1"]),
        ("💰", "Save an Emergency Fund", "Finance", 365,
         ["Set a savings target"]),
    ]

    for icon, name, cat, days, milestones in demo_goals:
        deadline = (today + timedelta(days=days)).isoformat()
        goal_id = goal_repo.add_goal(name, f"Work towards: {name}", icon, cat, deadline)
        for milestone_name in milestones:
            goal_repo.add_milestone(goal_id, milestone_name)

    # ── Demo Tasks ───────────────────────────────────────────────────────
    # ترکیبی از تسک دیروز (عقب‌افتاده)، امروز و روزهای آینده،
    # با اولویت و دسته‌بندی متنوع.
    demo_tasks = [
        ("Finish Python exercise", "Chapter 3 practice problems",
         "Learning", "High", today.isoformat()),
        ("Go for a run", "30 minutes jogging",
         "Fitness", "Medium", today.isoformat()),
        ("Reply to emails", "Clear out the inbox",
         "Work", "Low", today.isoformat()),
        ("Book dentist appointment", "Overdue — call the clinic",
         "Personal", "Medium", (today - timedelta(days=1)).isoformat()),
        ("Read chapter 5", "Continue reading current book",
         "Personal", "Low", (today + timedelta(days=1)).isoformat()),
        ("Weekly grocery shopping", "Milk, eggs, vegetables",
         "Personal", "Medium", (today + timedelta(days=2)).isoformat()),
    ]

    for name, desc, cat, prio, due_date in demo_tasks:
        task_repo.add_task(name, desc, cat, prio, due_date)

    # ── Demo Time Sessions ──────────────────────────────────────────────
    # category ها با گزینه‌های EditSessionDialog (Study/Work/Fitness/
    # Personal/Other) هم‌خوانی دارن.
    demo_sessions = [
        ("Python Study", "Study", 45 * 60),
        ("Deep Work Block", "Work", 50 * 60),
        ("Evening Run", "Fitness", 30 * 60),
        ("Journaling", "Personal", 15 * 60),
        ("Book Reading", "Study", 25 * 60),
    ]

    for name, cat, duration in demo_sessions:
        time_repo.add_time_session(name, cat, duration)


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
    
    sessions = time_repo.get_recent_sessions(limit=100000)
    for session in sessions:
        time_repo.delete_time_session(session.id)