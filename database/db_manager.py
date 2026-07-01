"""
db_manager.py
─────────────────────────────────────────────────────────────
مدیریت اتصال به دیتابیس SQLite + توابع CRUD برای هر جدول.
هر بار که برنامه اجرا می‌شه، اگه دیتابیس وجود نداشته باشه
از روی schema.sql ساخته می‌شه.
"""

import sqlite3
import os
from datetime import date, datetime, timedelta

from database.models import Habit, Goal, Milestone, Task, TimeSession

# مسیر فایل دیتابیس
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "smart_life.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    """یه اتصال جدید به دیتابیس برمی‌گردونه"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """دیتابیس و جداول رو می‌سازه (اگه وجود نداشته باشن)"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════════
# HABITS
# ════════════════════════════════════════════════════════════════

def add_habit(name, icon, category, frequency_type="daily", frequency_count=7):
    conn = get_connection()
    conn.execute(
        "INSERT INTO habits (name, icon, category, frequency_type, frequency_count) VALUES (?, ?, ?, ?, ?)",
        (name, icon, category, frequency_type, frequency_count)
    )
    conn.commit()
    conn.close()


def get_all_habits():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM habits ORDER BY id").fetchall()
    conn.close()
    return [Habit.from_row(r) for r in rows]


def delete_habit(habit_id):
    conn = get_connection()
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()


def toggle_habit_today(habit_id):
    """اگه امروز ثبت شده، حذفش کن. اگه نشده، ثبتش کن."""
    today = date.today().isoformat()
    conn = get_connection()
    exists = conn.execute(
        "SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?",
        (habit_id, today)
    ).fetchone()

    if exists:
        conn.execute("DELETE FROM habit_logs WHERE id = ?", (exists[0],))
    else:
        conn.execute(
            "INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
            (habit_id, today)
        )
    conn.commit()
    conn.close()


def is_habit_done_today(habit_id):
    today = date.today().isoformat()
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?",
        (habit_id, today)
    ).fetchone()
    conn.close()
    return row is not None


def get_week_progress(habit_id):
    """تعداد روزهای انجام‌شده در هفته جاری (شنبه تا الان) رو برمی‌گردونه"""
    today = date.today()
    # پیدا کردن شنبه این هفته (شروع هفته فارسی)
    weekday = (today.weekday() + 2) % 7  # تبدیل به شنبه=0
    start_of_week = today - timedelta(days=weekday)

    conn = get_connection()
    rows = conn.execute(
        "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date >= ?",
        (habit_id, start_of_week.isoformat())
    ).fetchone()
    conn.close()
    return rows[0]


def get_current_streak(habit_id):
    """تعداد روزهای متوالی انجام‌شده تا امروز رو حساب می‌کنه"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT log_date FROM habit_logs WHERE habit_id = ? ORDER BY log_date DESC",
        (habit_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]
    streak = 0
    expected = date.today()

    for d in dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == expected + timedelta(days=1):
            # هنوز امروز ثبت نشده، ولی دیروز ثبت شده -> ادامه بده
            continue
        else:
            break

    return streak


def get_best_streak(habit_id):
    """طولانی‌ترین رشته روزهای متوالی در کل تاریخچه"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT log_date FROM habit_logs WHERE habit_id = ? ORDER BY log_date ASC",
        (habit_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]
    best = current = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


# ════════════════════════════════════════════════════════════════
# GOALS
# ════════════════════════════════════════════════════════════════

def add_goal(name, description, icon, category, deadline=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO goals (name, description, icon, category, deadline) VALUES (?, ?, ?, ?, ?)",
        (name, description, icon, category, deadline)
    )
    conn.commit()
    conn.close()


def get_all_goals():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM goals ORDER BY id").fetchall()
    conn.close()
    return [Goal.from_row(r) for r in rows]


def delete_goal(goal_id):
    conn = get_connection()
    conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()


def update_goal(goal_id, name, description, icon, category, deadline=None):
    conn = get_connection()
    conn.execute(
        "UPDATE goals SET name = ?, description = ?, icon = ?, category = ?, deadline = ? WHERE id = ?",
        (name, description, icon, category, deadline, goal_id)
    )
    conn.commit()
    conn.close()


def delete_milestone(milestone_id):
    conn = get_connection()
    conn.execute("DELETE FROM milestones WHERE id = ?", (milestone_id,))
    conn.commit()
    conn.close()


def add_milestone(goal_id, name, sort_order=0):
    conn = get_connection()
    conn.execute(
        "INSERT INTO milestones (goal_id, name, sort_order) VALUES (?, ?, ?)",
        (goal_id, name, sort_order)
    )
    conn.commit()
    conn.close()


def get_milestones(goal_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM milestones WHERE goal_id = ? ORDER BY sort_order, id",
        (goal_id,)
    ).fetchall()
    conn.close()
    return [Milestone.from_row(r) for r in rows]


def toggle_milestone(milestone_id):
    conn = get_connection()
    row = conn.execute("SELECT done FROM milestones WHERE id = ?", (milestone_id,)).fetchone()
    new_val = 0 if row[0] else 1
    conn.execute("UPDATE milestones SET done = ? WHERE id = ?", (new_val, milestone_id))
    conn.commit()
    conn.close()


def get_goal_progress_percent(goal_id):
    """درصد پیشرفت هدف بر اساس مایلستون‌های انجام‌شده"""
    milestones = get_milestones(goal_id)
    if not milestones:
        return 0
    done = sum(1 for m in milestones if m.done)
    return round(done / len(milestones) * 100)


# ════════════════════════════════════════════════════════════════
# TASKS
# ════════════════════════════════════════════════════════════════

def add_task(name, description, category, priority, due_date=None, due_time=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (name, description, category, priority, due_date, due_time) VALUES (?, ?, ?, ?, ?, ?)",
        (name, description, category, priority, due_date, due_time)
    )
    conn.commit()
    conn.close()


def get_all_tasks(done=None):
    """done=None یعنی همه، done=True/False یعنی فیلتر شده"""
    conn = get_connection()
    if done is None:
        rows = conn.execute("SELECT * FROM tasks ORDER BY due_date, due_time").fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE done = ? ORDER BY due_date, due_time",
            (1 if done else 0,)
        ).fetchall()
    conn.close()
    return [Task.from_row(r) for r in rows]


def update_task(task_id, name, description, category, priority, due_date=None, due_time=None):
    conn = get_connection()
    conn.execute(
        """UPDATE tasks
           SET name = ?, description = ?, category = ?, priority = ?, due_date = ?, due_time = ?
           WHERE id = ?""",
        (name, description, category, priority, due_date, due_time, task_id)
    )
    conn.commit()
    conn.close()


def toggle_task(task_id):
    conn = get_connection()
    row = conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    new_val = 0 if row[0] else 1
    conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_val, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════════
# TIME SESSIONS
# ════════════════════════════════════════════════════════════════

def update_time_session(session_id, name, category, duration_seconds):
    conn = get_connection()
    conn.execute(
        "UPDATE time_sessions SET name = ?, category = ?, duration = ? WHERE id = ?",
        (name, category, duration_seconds, session_id)
    )
    conn.commit()
    conn.close()


def delete_time_session(session_id):
    conn = get_connection()
    conn.execute("DELETE FROM time_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


def update_time_session(session_id, name, category):
    conn = get_connection()
    conn.execute(
        "UPDATE time_sessions SET name = ?, category = ? WHERE id = ?",
        (name, category, session_id)
    )
    conn.commit()
    conn.close()


def delete_time_session(session_id):
    conn = get_connection()
    conn.execute("DELETE FROM time_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


def add_time_session(name, category, duration_seconds, session_date=None):
    if session_date is None:
        session_date = date.today().isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO time_sessions (name, category, duration, session_date) VALUES (?, ?, ?, ?)",
        (name, category, duration_seconds, session_date)
    )
    conn.commit()
    conn.close()


def get_sessions_today():
    today = date.today().isoformat()
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM time_sessions WHERE session_date = ? ORDER BY created_at DESC",
        (today,)
    ).fetchall()
    conn.close()
    return [TimeSession.from_row(r) for r in rows]


def get_recent_sessions(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM time_sessions ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [TimeSession.from_row(r) for r in rows]


def get_total_time_today():
    """مجموع ثانیه‌های امروز"""
    today = date.today().isoformat()
    conn = get_connection()
    row = conn.execute(
        "SELECT SUM(duration) FROM time_sessions WHERE session_date = ?",
        (today,)
    ).fetchone()
    conn.close()
    return row[0] or 0


def get_weekly_activity():
    """برمی‌گرداند: [(day_name, total_hours), ...] برای ۷ روز گذشته"""
    today = date.today()
    weekday = (today.weekday() + 2) % 7
    start_of_week = today - timedelta(days=weekday)

    conn = get_connection()
    result = []
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        d = start_of_week + timedelta(days=i)
        row = conn.execute(
            "SELECT SUM(duration) FROM time_sessions WHERE session_date = ?",
            (d.isoformat(),)
        ).fetchone()
        total_hours = (row[0] or 0) / 3600
        result.append((day_names[i], round(total_hours, 1)))
    conn.close()
    return result


def get_time_distribution():
    """برمی‌گرداند: [(category, total_hours), ...]"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT category, SUM(duration) FROM time_sessions GROUP BY category"
    ).fetchall()
    conn.close()
    return [(cat, round((dur or 0) / 3600, 1)) for cat, dur in rows]

def get_habit_log_count(habit_id, start_date, end_date):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT COUNT(*)
        FROM habit_logs
        WHERE habit_id = ?
        AND log_date BETWEEN ? AND ?
        """,
        (habit_id, start_date, end_date)
    ).fetchone()

    conn.close()

    return row[0]