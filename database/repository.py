# database/repository.py

from database import db_manager as db


# ==========================================================
# Goals
# ==========================================================

class GoalRepository:
    def get_all_goals(self):
        return db.get_all_goals()

    def add_goal(self, name, description, icon, category, deadline):
        return db.add_goal(
            name=name,
            description=description,
            icon=icon,
            category=category,
            deadline=deadline,
        )

    def update_goal(self, goal_id, name, description, icon, category, deadline):
        return db.update_goal(
            goal_id,
            name,
            description,
            icon,
            category,
            deadline,
        )

    def delete_goal(self, goal_id):
        return db.delete_goal(goal_id)

    def get_goal_progress_percent(self, goal_id):
        return db.get_goal_progress_percent(goal_id)

    def get_milestones(self, goal_id):
        return db.get_milestones(goal_id)

    def add_milestone(self, goal_id, name):
        return db.add_milestone(goal_id, name)

    def toggle_milestone(self, milestone_id):
        return db.toggle_milestone(milestone_id)

    def delete_milestone(self, milestone_id):
        return db.delete_milestone(milestone_id)


# ==========================================================
# Habits
# ==========================================================

class HabitRepository:
    def get_all_habits(self):
        return db.get_all_habits()

    def is_habit_done_today(self, habit_id):
        return db.is_habit_done_today(habit_id)

    def get_habit_log_count(self, habit_id, start_date, end_date):
        return db.get_habit_log_count(
            habit_id,
            start_date,
            end_date,
        )
    
    def count_logs_in_range(self, habit_id, start_date, end_date):
        return db.count_habit_logs_in_range(
            habit_id,
            start_date,
            end_date
        )
    def get_current_streak(self, habit_id):
        return db.get_current_streak(habit_id)
    
    def get_week_progress(self, habit_id):
        return db.get_week_progress(habit_id)


# ==========================================================
# Tasks
# ==========================================================

class TaskRepository:
    def get_all_tasks(self, done=None):
        return db.get_all_tasks(done=done)


# ==========================================================
# Analytics
# ==========================================================

class AnalyticsRepository:
    def get_total_time_today(self):
        return db.get_total_time_today()

    def get_habits_done_count_on_date(self, habits, target_date):
        return db.get_habits_done_count_on_date(habits, target_date)

    def get_focus_duration_on_date(self, target_date):
        return db.get_focus_duration_on_date(target_date)
    
    def get_focus_duration_in_range(self, start_date, end_date):
        return db.get_focus_duration_in_range(
        start_date,
        end_date,
    )

    def get_weekly_activity(self):
        return db.get_weekly_activity()


# Singleton instances
goal_repo = GoalRepository()
habit_repo = HabitRepository()
task_repo = TaskRepository()
analytics_repo = AnalyticsRepository()