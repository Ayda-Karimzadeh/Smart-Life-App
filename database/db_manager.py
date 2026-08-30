"""
db_manager.py
─────────────────────────────────────────────────────────────
مدیریت اتصال به دیتابیس SQLite + توابع CRUD برای هر جدول.
هر بار که برنامه اجرا می‌شه، اگه دیتابیس وجود نداشته باشه
از روی schema.sql ساخته می‌شه.
"""

import sqlite3
import os
from datetime import date, timedelta
from database.models import Habit, Goal, Milestone, Task, TimeSession
from core.dates import start_of_week, end_of_week, get_weekday_labels_short
from config.paths import DB_PATH, SCHEMA_PATH

CURRENT_SCHEMA_VERSION = 1


def _migrate(conn):
    row = conn.execute(
        "SELECT version FROM schema_version WHERE id = 1"
    ).fetchone()
    version = row[0] if row else 0

    if version > CURRENT_SCHEMA_VERSION:
        raise RuntimeError(
            f"Database schema version {version} is newer than supported version "
            f"{CURRENT_SCHEMA_VERSION}"
        )

    if version == 0:
        conn.execute(
            "INSERT INTO schema_version (id, version) VALUES (1, ?)",
            (CURRENT_SCHEMA_VERSION,),
        )


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the schema and record its version for future migrations."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    try:
        with SCHEMA_PATH.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
        _migrate(conn)
        conn.commit()
    finally:
        conn.close()


# ════════════════════════════════════════════════════════════════
# HABITS
# ════════════════════════════════════════════════════════════════

def add_habit(name, icon, category, frequency_type="daily", frequency_count=7):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO habits (name, icon, category, frequency_type, frequency_count) VALUES (?, ?, ?, ?, ?)",
        (name, icon, category, frequency_type, frequency_count)
    )
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()
    return habit_id


def get_all_habits():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM habits ORDER BY id").fetchall()
    conn.close()
    return [Habit.from_row(r) for r in rows]


def update_habit(habit_id, name, icon, category, frequency_type="daily", frequency_count=7):
    conn = get_connection()
    conn.execute(
        "UPDATE habits SET name = ?, icon = ?, category = ?, frequency_type = ?, frequency_count = ? WHERE id = ?",
        (name, icon, category, frequency_type, frequency_count, habit_id)
    )
    conn.commit()
    conn.close()


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


def add_habit_log(habit_id, log_date):
    """برخلاف toggle_habit_today، این یکی برای هر تاریخ دلخواهی کار می‌کنه
    (نه فقط امروز) و اگه از قبل ثبت شده باشه، دوباره اضافه نمی‌کنه.
    عمدتاً برای seed کردن داده‌ی گذشته (مثل demo data) استفاده می‌شه."""
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?",
            (habit_id, log_date)
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
                (habit_id, log_date)
            )
            conn.commit()
    finally:
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
    week_start = start_of_week()
    week_end = end_of_week()

    conn = get_connection()
    rows = conn.execute(
        "SELECT COUNT(*) FROM habit_logs "
        "WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
        (habit_id, week_start.isoformat(), week_end.isoformat())
    ).fetchone()
    conn.close()
    return rows[0]


def get_habit_log_dates(habit_id, start_date=None, end_date=None, order="ASC"):
    conn = get_connection()
    try:
        query = "SELECT log_date FROM habit_logs WHERE habit_id = ?"
        params = [habit_id]
        if start_date:
            query += " AND log_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND log_date <= ?"
            params.append(end_date)
        if order.upper() not in ("ASC", "DESC"):
            order = "ASC"
        query += f" ORDER BY log_date {order.upper()}"
        rows = conn.execute(query, params).fetchall()
        return [r[0] for r in rows]
    finally:
        conn.close()


def get_habit_frequency_count(habit_id):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT frequency_count FROM habits WHERE id = ?",
            (habit_id,)
        ).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def get_habit_created_at(habit_id):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT created_at FROM habits WHERE id = ?",
            (habit_id,)
        ).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def count_habit_logs_in_range(habit_id, start_date, end_date):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
            (habit_id, start_date, end_date)
        ).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


# ════════════════════════════════════════════════════════════════
# GOALS
# ════════════════════════════════════════════════════════════════

def add_goal(name, description, icon, category, deadline=None):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO goals 
        (name, description, icon, category, deadline)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, icon, category, deadline)
    )

    conn.commit()

    goal_id = cursor.lastrowid

    conn.close()

    return goal_id


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
        """
        INSERT INTO milestones 
        (goal_id, name, sort_order)
        VALUES (?, ?, ?)
        """,
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
    try:
        row = conn.execute("SELECT done FROM milestones WHERE id = ?", (milestone_id,)).fetchone()
        if not row:
            return
        new_val = 0 if row[0] else 1
        conn.execute("UPDATE milestones SET done = ? WHERE id = ?", (new_val, milestone_id))
        conn.commit()
    finally:
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
    try:
        row = conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return
        new_val = 0 if row[0] else 1
        conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_val, task_id))
        conn.commit()
    finally:
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
    """برمی‌گرداند: [(day_name, total_hours), ...] برای ۷ روز هفته جاری (شنبه تا جمعه)"""
    week_start = start_of_week()
    weekday_labels = get_weekday_labels_short()

    conn = get_connection()
    result = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        row = conn.execute(
            "SELECT SUM(duration) FROM time_sessions WHERE session_date = ?",
            (d.isoformat(),)
        ).fetchone()
        total_hours = (row[0] or 0) / 3600
        result.append((weekday_labels[i], round(total_hours, 1)))
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

def get_habits_done_count_on_date(target_date) -> int:
    """تعداد عادت‌های انجام‌شده در یک تاریخ مشخص."""

    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT COUNT(DISTINCT habit_id)
            FROM habit_logs
            WHERE log_date = ?
            """,
            (target_date.isoformat(),)
        ).fetchone()

        return row[0] or 0

    finally:
        conn.close()

def get_focus_duration_on_date(target_date) -> float:
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT SUM(duration)
            FROM time_sessions
            WHERE session_date = ?
            """,
            (target_date.isoformat(),)
        ).fetchone()

        return (row[0] or 0) / 3600

    finally:
        conn.close()

def get_focus_duration_in_range(start_date: str, end_date: str) -> float:
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT SUM(duration)
            FROM time_sessions
            WHERE session_date BETWEEN ? AND ?
            """,
            (start_date, end_date)
        ).fetchone()

        return (row[0] or 0) / 3600

    finally:
        conn.close()


# ════════════════════════════════════════════════════════════════
# APP SETTINGS
# ════════════════════════════════════════════════════════════════

def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = ?",
            (key,),
        ).fetchone()
        return row[0] if row else default
    finally:
        conn.close()


def set_setting(key: str, value: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO app_settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


def has_any_habit_logs() -> bool:
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) FROM habit_logs").fetchone()
        return (row[0] or 0) > 0
    finally:
        conn.close()


def has_any_time_sessions() -> bool:
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) FROM time_sessions").fetchone()
        return (row[0] or 0) > 0
    finally:
        conn.close()