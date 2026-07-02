from datetime import date, timedelta
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
)
from core.streak_engine import weekly_streak as streak_weekly_streak

# Consistency Score
def consistency_score(habit_id: int, days: int = 30) -> float:
    today = date.today()
    start = today - timedelta(days=days - 1)
    done = habit_repo.get_habit_log_count(
        habit_id,   start.isoformat(), today.isoformat()
    )
    return round(done / days * 100, 1)

def overall_consistency(days: int = 30) -> float:
    habits = habit_repo.get_all_habits()
    if not habits:
        return 0.0
    scores = [consistency_score(h.id, days) for h in habits]
    return round(sum(scores) / len(scores), 1)

# Productivity Score (0-100)
def productivity_score(target_focus_hours: int = 4) -> int:
    habits = habit_repo.get_all_habits()
    goals  = goal_repo.get_all_goals()
    tasks  = task_repo.get_all_tasks()
    focus  = analytics_repo.get_total_time_today()

    if habits:
        done_today  = sum(1 for h in habits if habit_repo.is_habit_done_today(h.id))
        habit_score = done_today / len(habits) * 100
    else:
        habit_score = 0

    if goals:
        goal_score = sum(goal_repo.get_goal_progress_percent(g.id) for g in goals) / len(goals)
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
    # گزارش کامل هفته جاری

    today      = date.today()
    weekday    = today.weekday()   # 0=Mon
    week_start = today - timedelta(days=weekday)

    habits = habit_repo.get_all_habits()
    tasks  = task_repo.get_all_tasks()

    day_names    = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    habit_scores = []
    focus_hours  = []
    tasks_done   = []

    for i in range(7):
        d = week_start + timedelta(days=i)

        # habit score
        if habits:
            done = _habits_done_on(habits, d)
            habit_scores.append(round(done / len(habits) * 100))
        else:
            habit_scores.append(0)

        # focus hours
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
    return streak_weekly_streak(habit_id)

# Strengths & Weaknesses
def strengths_and_weaknesses() -> dict:
    """
    بر اساس consistency_score هر عادت，
    قوی‌ترین‌ها و ضعیف‌ترین‌ها رو برمی‌گردونه.

    برمی‌گردونه:
    {
        "strengths": [{"name": "ورزش", "score": 90}, ...],
        "weaknesses": [{"name": "مطالعه", "score": 30}, ...],
    }
    """
    habits = habit_repo.get_all_habits()
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

# توابع کمکی داخلی
def _habits_done_on(habits, target_date: date) -> int:
    """تعداد عادت‌هایی که در یه روز خاص انجام شدن"""
    return habit_repo.get_habits_done_count_on_date(habits, target_date)

def _focus_on(target_date: date) -> float:
    """ساعت‌های Focus یه روز خاص"""
    return analytics_repo.get_focus_duration_on_date(target_date)
