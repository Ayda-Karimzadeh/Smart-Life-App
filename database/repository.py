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
    def add_habit(self, name, icon, category, frequency_type="daily", frequency_count=7):
        return db.add_habit(name, icon, category, frequency_type, frequency_count)

    def update_habit(self, habit_id, name, icon, category, frequency_type="daily", frequency_count=7):
        return db.update_habit(habit_id, name, icon, category, frequency_type, frequency_count)

    def delete_habit(self, habit_id):
        return db.delete_habit(habit_id)

    def toggle_habit_today(self, habit_id):
        return db.toggle_habit_today(habit_id)

    def log_habit_on_date(self, habit_id, log_date):
        """ثبت لاگ یه عادت برای تاریخ دلخواه (نه فقط امروز).
        عمدتاً برای seed کردن داده‌ی گذشته (مثل demo data) استفاده می‌شه."""
        return db.add_habit_log(habit_id, log_date)

    def get_all_habits(self):
        return db.get_all_habits()

    def is_habit_done_today(self, habit_id):
        return db.is_habit_done_today(habit_id)

    def get_habit_log_dates(self, habit_id, start_date=None, end_date=None, order="ASC"):
        return db.get_habit_log_dates(habit_id, start_date, end_date, order)

    def count_logs_in_range(self, habit_id, start_date, end_date):
        return db.count_habit_logs_in_range(habit_id, start_date, end_date)

    def get_habit_log_count(self, habit_id, start_date, end_date):
        return self.count_logs_in_range(habit_id, start_date, end_date)

    def get_habit_frequency_count(self, habit_id):
        return db.get_habit_frequency_count(habit_id)

    def get_habit_created_at(self, habit_id):
        return db.get_habit_created_at(habit_id)

    def get_current_streak(self, habit_id):
        from core.streak_engine import daily_streak
        return daily_streak(habit_id)

    def get_best_streak(self, habit_id):
        from core.streak_engine import best_daily_streak
        return best_daily_streak(habit_id)

    def get_habits_done_count_on_date(self, target_date):
        return db.get_habits_done_count_on_date(target_date)

    def get_week_progress(self, habit_id):
        return db.get_week_progress(habit_id)


# ==========================================================
# Tasks
# ==========================================================

class TaskRepository:
    def add_task(self, name, description, category, priority, due_date=None, due_time=None):
        return db.add_task(name, description, category, priority, due_date, due_time)

    def get_all_tasks(self, done=None):
        return db.get_all_tasks(done=done)

    def update_task(self, task_id, name, description, category, priority, due_date=None, due_time=None):
        return db.update_task(task_id, name, description, category, priority, due_date, due_time)

    def toggle_task(self, task_id):
        return db.toggle_task(task_id)

    def delete_task(self, task_id):
        return db.delete_task(task_id)


# ==========================================================
# Time Sessions
# ==========================================================

class TimeSessionRepository:
    def add_time_session(self, name, category, duration_seconds, session_date=None):
        return db.add_time_session(name, category, duration_seconds, session_date)

    def update_time_session(self, session_id, name, category, duration_seconds):
        return db.update_time_session(session_id, name, category, duration_seconds)

    def delete_time_session(self, session_id):
        return db.delete_time_session(session_id)

    def get_sessions_today(self):
        return db.get_sessions_today()

    def get_recent_sessions(self, limit=10):
        return db.get_recent_sessions(limit=limit)

    def get_total_time_today(self):
        return db.get_total_time_today()

    def get_weekly_activity(self):
        return db.get_weekly_activity()

    def get_time_distribution(self):
        return db.get_time_distribution()


# ==========================================================
# Analytics
# ==========================================================

class AnalyticsRepository(TimeSessionRepository):
    def get_habits_done_count_on_date(self, target_date):
        return db.get_habits_done_count_on_date(target_date)

    def get_focus_duration_on_date(self, target_date):
        return db.get_focus_duration_on_date(target_date)

    def get_focus_duration_in_range(self, start_date, end_date):
        return db.get_focus_duration_in_range(start_date, end_date)

    def has_any_habit_logs(self):
        return db.has_any_habit_logs()

    def has_any_time_sessions(self):
        return db.has_any_time_sessions()


# ==========================================================
# App Settings
# ==========================================================

class SettingsRepository:
    def get(self, key: str, default: str = "") -> str:
        return db.get_setting(key, default)

    def set(self, key: str, value: str) -> None:
        db.set_setting(key, value)

    def get_user_name(self) -> str:
        return self.get("user_name", "")

    def set_user_name(self, name: str) -> None:
        self.set("user_name", name)

    def is_onboarding_completed(self) -> bool:
        return self.get("onboarding_completed") == "1"

    def mark_onboarding_completed(self) -> None:
        self.set("onboarding_completed", "1")


# Singleton instances
goal_repo = GoalRepository()
habit_repo = HabitRepository()
task_repo = TaskRepository()
time_repo = TimeSessionRepository()
analytics_repo = AnalyticsRepository()
settings_repo = SettingsRepository()