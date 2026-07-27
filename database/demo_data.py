"""Demo data seeder for first-time user experience."""

from datetime import date, timedelta
from database.repository import habit_repo, goal_repo, task_repo, time_repo


def seed_demo_data():
    """Seed demo data for a better first-time experience."""
    from datetime import datetime
    
    today = date.today()
    
    # Demo Habits
    demo_habits = [
        ("🧘", "Morning Meditation", "Mindfulness", "daily", 7),
        ("💪", "Exercise", "Fitness", "weekly", 3),
        ("📚", "Reading", "Personal Growth", "daily", 7),
        ("💧", "Drink Water", "Health", "daily", 8),
    ]
    
    for icon, name, cat, freq_type, freq_count in demo_habits:
        habit = habit_repo.add_habit(name, icon, cat, freq_type, freq_count)
        # Add some completed logs for the past week
        for days_ago in range(7):
            log_date = today - timedelta(days=days_ago)
            if days_ago < 5:  # Completed 5 out of 7 days
                habit_repo.log_habit(habit.id, log_date.isoformat())
    
    # Demo Goals
    demo_goals = [
        ("🎯", "Learn Python", "Learning", 90),
        ("💪", "Get Fit", "Fitness", 180),
        ("📖", "Read 12 Books", "Personal", 365),
    ]
    
    for icon, name, cat, days in demo_goals:
        deadline = (today + timedelta(days=days)).isoformat()
        goal = goal_repo.add_goal(name, f"Work towards: {name}", icon, cat, deadline)
        # Add some progress
        goal_repo.add_milestone(goal.id, "Started learning basics")
        goal_repo.add_milestone(goal.id, "Completed first project")
    
    # Demo Tasks
    demo_tasks = [
        ("Complete Python tutorial", "Finish the basics course", "Learning", "High", today.isoformat()),
        ("Go for a run", "30 minutes jogging", "Fitness", "Medium", today.isoformat()),
        ("Read chapter 5", "Continue reading book", "Personal", "Low", (today + timedelta(days=1)).isoformat()),
    ]
    
    for name, desc, cat, prio, due_date in demo_tasks:
        task_repo.add_task(name, desc, cat, prio, due_date)
    
    # Demo Time Sessions
    demo_sessions = [
        ("Python Study", "Learning", 45 * 60),  # 45 minutes
        ("Reading", "Personal", 30 * 60),  # 30 minutes
        ("Exercise", "Fitness", 60 * 60),  # 1 hour
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
    
    sessions = time_repo.get_all_sessions()
    for session in sessions:
        time_repo.delete_session(session.id)
