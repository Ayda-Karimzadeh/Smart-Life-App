from datetime import date, timedelta
from database import db_manager as db

# Consistency Score
def consistency_score(habit_id: int, days: int = 30) -> float:
    today = date.today()
    start = today - timedelta(days=days - 1)
    done = db.get_habit_log_count(
        habit_id,   start.isoformat(), today.isoformat()
    )
    return round(done / days * 100, 1)

def overall_consistency(days: int = 30) -> float:
    habits = db.get_all_habits()
    if not habits:
        return 0.0
    scores = [consistency_score(h.id, days) for h in habits]
    return round(sum(scores) / len(scores), 1)

# Productivity Score (0-100)
def productivity_score(target_focus_hours: int = 4) -> int:
    habits = db.get_all_habits()
    goals  = db.get_all_goals()
    tasks  = db.get_all_tasks()
    focus  = db.get_total_time_today()

    if habits:
        done_today  = sum(1 for h in habits if db.is_habit_done_today(h.id))
        habit_score = done_today / len(habits) * 100
    else:
        habit_score = 0

    if goals:
        goal_score = sum(db.get_goal_progress_percent(g.id) for g in goals) / len(goals)
    else:
        goal_score = 0

    if tasks:
        done_tasks = sum(1 for t in tasks if t.done)
        task_score = done_tasks / len(tasks) * 100
    else:
        task_score = 0

    target_focus = target_focus_hours * 3600   # hours to seconds
    focus_score  = min(focus / target_focus * 100, 100)
    weights = {
        "habit": 0.40,
        "goal":  0.30,
        "task":  0.20,
        "focus": 0.10
    }
    total = (
        habit_score * weights["habit"] +
        goal_score  * weights["goal"] +
        task_score  * weights["task"] +
        focus_score * weights["focus"]
    )
    return round(total)

# Weekly Report
def weekly_report() -> dict:
    """
    گزارش کامل هفته جاری.

    برمی‌گردونه:
    {
        "habit_scores":  [80, 60, 100, ...],   # ۷ روز
        "focus_hours":   [2.5, 1.0, 3.0, ...], # ۷ روز
        "tasks_done":    [2, 1, 3, ...],        # ۷ روز
        "days":          ["Mon", "Tue", ...],
        "best_day":      "Wednesday",
        "worst_day":     "Monday",
        "avg_habit_pct": 74,
        "total_focus":   12.5,
        "tasks_completed": 8,
    }
    """
    today      = date.today()
    weekday    = today.weekday()   # 0=Mon
    week_start = today - timedelta(days=weekday)

    habits = db.get_all_habits()
    tasks  = db.get_all_tasks()

    day_names    = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    habit_scores = []
    focus_hours  = []
    tasks_done   = []

    for i in range(7):
        d = week_start + timedelta(days=i)

        # habit score این روز
        if habits:
            done = _habits_done_on(habits, d)
            habit_scores.append(round(done / len(habits) * 100))
        else:
            habit_scores.append(0)

        # focus hours این روز
        focus_hours.append(round(_focus_on(d), 1))

        # تسک‌های انجام‌شده این روز (due_date = این روز و done=True)
        td = sum(1 for t in tasks if t.due_date == d.isoformat() and t.done)
        tasks_done.append(td)

    # بهترین و بدترین روز بر اساس habit score
    valid_days = [(s, day_names[i]) for i, s in enumerate(habit_scores) if s > 0]
    best_day   = max(valid_days, key=lambda x: x[0])[1] if valid_days else "—"
    worst_day  = min(valid_days, key=lambda x: x[0])[1] if valid_days else "—"

    return {
        "habit_scores":    habit_scores,
        "focus_hours":     focus_hours,
        "tasks_done":      tasks_done,
        "days":            day_names,
        "best_day":        best_day,
        "worst_day":       worst_day,
        "avg_habit_pct":   round(sum(habit_scores) / 7) if habit_scores else 0,
        "total_focus":     round(sum(focus_hours), 1),
        "tasks_completed": sum(tasks_done),
    }

# Streak Engine (Weekly)
def weekly_streak(habit_id: int) -> int:
    """
    تعداد هفته‌های متوالی که هدف frequency برآورده شده.

    مثال: عادت "ورزش ۳ بار در هفته":
    - هفته جاری: ۲ بار → streak شکسته
    - هفته قبل: ۳ بار → streak = 1
    - دو هفته قبل: ۴ بار → streak = 2
    """
    conn  = db.get_connection()
    habit = conn.execute("SELECT frequency_count FROM habits WHERE id = ?", (habit_id,)).fetchone()
    conn.close()

    if not habit:
        return 0

    target = habit[0]
    streak = 0
    today  = date.today()

    for week_offset in range(52):  # حداکثر ۵۲ هفته به عقب
        week_end   = today - timedelta(days=today.weekday() + week_offset * 7)
        week_start = week_end - timedelta(days=6)

        conn = db.get_connection()
        row  = conn.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
            (habit_id, week_start.isoformat(), week_end.isoformat())
        ).fetchone()
        conn.close()

        done = row[0] if row else 0

        if done >= target:
            streak += 1
        else:
            break

    return streak


# ════════════════════════════════════════════════════════════
# Strengths & Weaknesses
# ════════════════════════════════════════════════════════════

def strengths_and_weaknesses() -> dict:
    """
    بر اساس consistency_score هر عادت،
    قوی‌ترین‌ها و ضعیف‌ترین‌ها رو برمی‌گردونه.

    برمی‌گردونه:
    {
        "strengths": [{"name": "ورزش", "score": 90}, ...],
        "weaknesses": [{"name": "مطالعه", "score": 30}, ...],
    }
    """
    habits = db.get_all_habits()
    if not habits:
        return {"strengths": [], "weaknesses": []}

    scores = []
    for h in habits:
        score = consistency_score(h.id, 30)
        scores.append({"name": h.name, "icon": h.icon, "score": score})

    scores.sort(key=lambda x: x["score"], reverse=True)

    return {
        "strengths":  [s for s in scores if s["score"] >= 70][:3],
        "weaknesses": [s for s in scores if s["score"] < 70][-3:],
    }


# ════════════════════════════════════════════════════════════
# توابع کمکی داخلی
# ════════════════════════════════════════════════════════════

def _habits_done_on(habits, target_date: date) -> int:
    """تعداد عادت‌هایی که در یه روز خاص انجام شدن"""
    conn  = db.get_connection()
    count = 0
    for h in habits:
        row = conn.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date = ?",
            (h.id, target_date.isoformat())
        ).fetchone()
        if row and row[0] > 0:
            count += 1
    conn.close()
    return count


def _focus_on(target_date: date) -> float:
    """ساعت‌های Focus یه روز خاص"""
    conn = db.get_connection()
    row  = conn.execute(
        "SELECT SUM(duration) FROM time_sessions WHERE session_date = ?",
        (target_date.isoformat(),)
    ).fetchone()
    conn.close()
    return (row[0] or 0) / 3600