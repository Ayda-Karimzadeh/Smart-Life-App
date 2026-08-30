from datetime import date, timedelta
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
)
from core.streak_engine import daily_streak, weekly_streak as streak_weekly_streak
from core.dates import start_of_week, get_weekday_labels_short
from core.language_manager import tr


def _habit_created_date(habit) -> date | None:
    created_at = getattr(habit, "created_at", None)
    if not created_at:
        return None

    try:
        return date.fromisoformat(created_at)
    except (TypeError, ValueError):
        return None


def _weekly_expected_count(habit, period_start: date, period_end: date) -> int:
    """Return weekly targets prorated to the habit's active days."""
    created_date = _habit_created_date(habit)
    active_start = max(period_start, created_date) if created_date else period_start
    active_days = (period_end - active_start).days + 1

    if active_days <= 0:
        return 0

    return min(int(habit.frequency_count), active_days)


# Consistency Score
def consistency_score(habit_id: int, days: int = 30) -> float:
    today = date.today()
    start = today - timedelta(days=days - 1)
    habit = next((h for h in habit_repo.get_all_habits() if h.id == habit_id), None)
    if habit is None or habit.frequency_count <= 0:
        return 0.0

    created_date = _habit_created_date(habit)
    tracking_start = max(start, created_date) if created_date else start

    done = habit_repo.get_habit_log_count(
        habit_id, tracking_start.isoformat(), today.isoformat()
    )
    if habit.frequency_type == "weekly":
        expected = 0
        week_start = start_of_week(start)
        while week_start <= today:
            week_end = min(week_start + timedelta(days=6), today)
            expected += _weekly_expected_count(habit, week_start, week_end)
            week_start += timedelta(weeks=1)
    else:
        expected = max((today - tracking_start).days + 1, 0)

    if expected <= 0:
        return 0.0

    return round(done / expected * 100, 1)

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
    today = date.today().isoformat()

    if habits:
        done_today  = sum(1 for h in habits if habit_repo.is_habit_done_today(h.id))
        habit_score = done_today / len(habits) * 100
    else:
        habit_score = 0

    if goals:
        goal_score = sum(goal_repo.get_goal_progress_percent(g.id) for g in goals) / len(goals)
    else:
        goal_score = 0

    relevant_tasks = [
        t for t in tasks
            if getattr(t, "due_date", None) == today
    ]
    if relevant_tasks:
        done_tasks = sum(1 for t in relevant_tasks if t.done)
        task_score = done_tasks / len(relevant_tasks) * 100
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
    today = date.today()
    week_start = start_of_week(today)

    habits = habit_repo.get_all_habits()
    tasks  = task_repo.get_all_tasks()

    day_names    = get_weekday_labels_short()
    habit_scores = []
    focus_hours  = []
    tasks_done   = []

    for i in range(7):
        d = week_start + timedelta(days=i)

        # habit score
        if habits:
            completed_ratios = []
            for h in habits:
                created_date = _habit_created_date(h)
                if created_date and d < created_date:
                    continue

                if h.frequency_type == "weekly":
                    active_week_start = max(week_start, created_date) if created_date else week_start
                    active_days = (week_start + timedelta(days=6) - active_week_start).days + 1
                    target = min(int(h.frequency_count), active_days) / active_days
                else:
                    target = 1
                done_today = habit_repo.count_logs_in_range(h.id, d.isoformat(), d.isoformat())
                completed_ratios.append(min(done_today / target, 1.0) * 100)
            habit_scores.append(
                round(sum(completed_ratios) / len(completed_ratios))
                if completed_ratios else 0
            )
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
    بر اساس consistency_score هر عادت،
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

    ranked = sorted(scores, key=lambda x: x["score"], reverse=True)
    strengths = ranked[:3]
    weaknesses = sorted(
        [s for s in ranked if s["score"] < 70],
        key=lambda x: x["score"]
    )[:3]

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
    }

# توابع کمکی داخلی
def _habits_done_on(habits, target_date: date) -> int:
    """تعداد عادت‌هایی که در یه روز خاص انجام شدن"""
    return habit_repo.get_habits_done_count_on_date(target_date)

def _focus_on(target_date: date) -> float:
    """ساعت‌های Focus یه روز خاص"""
    return analytics_repo.get_focus_duration_on_date(target_date)

def get_key_insight() -> dict | None:
    """
    یک Insight برجسته برای Dashboard برمی‌گرداند.

    اولویت:
    1. Streak قوی
    2. Goal نزدیک به تکمیل
    3. اگر داده کافی نباشد → None

    خروجی:
    {
        "type": "streak",
        "icon": "🔥",
        "title": "...",
        "message": "...",
        "value": 12
    }
    """

    habits = habit_repo.get_all_habits()
    goals = goal_repo.get_all_goals()

    # ─────────────────────────────────────────────
    # 1. بهترین Streak
    # ─────────────────────────────────────────────
    best_habit = None
    best_streak = 0

    for habit in habits:
        streak = daily_streak(habit.id)

        if streak > best_streak:
            best_streak = streak
            best_habit = habit

    if best_habit and best_streak >= 3:
        return {
            "type": "streak",
            "icon": "🔥",
            "title": tr("key_insight"),
            "message": tr("insight_streak").format(
                habit=best_habit.name,
                streak=best_streak
            ),
            "value": best_streak,
        }

    # ─────────────────────────────────────────────
    # 2. نزدیک‌ترین Goal
    # ─────────────────────────────────────────────
    almost_done = []

    for goal in goals:
        pct = goal_repo.get_goal_progress_percent(goal.id)

        if 70 <= pct < 100:
            almost_done.append((pct, goal))

    if almost_done:
        pct, goal = max(almost_done, key=lambda x: x[0])

        return {
            "type": "goal",
            "icon": "🎯",
            "title": tr("key_insight"),
            "message": tr("insight_goal_almost_done").format(
                goal=goal.name,
                progress=pct
            ),
            "value": pct,
        }

    # ─────────────────────────────────────────────
    # 3. داده کافی نیست
    # ─────────────────────────────────────────────
    return None