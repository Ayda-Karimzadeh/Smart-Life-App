"""
core/streak_engine.py
─────────────────────────────────────────────────────────────
منطق محاسبه Streak برای عادت‌های روزانه و هفتگی.
کاملاً مستقل از UI — فقط از repository داده می‌گیره و عدد برمی‌گردونه.
"""

from datetime import date, timedelta, datetime

from database.repository import habit_repo
from core.dates import start_of_week, end_of_week


# ════════════════════════════════════════════════════════════
# Daily Streak
# ════════════════════════════════════════════════════════════

def daily_streak(habit_id: int) -> int:
    rows = habit_repo.get_habit_log_dates(habit_id, order="DESC")
    if not rows:
        return 0

    dates = [datetime.strptime(r, "%Y-%m-%d").date() for r in rows]
    streak = 0
    expected = date.today()

    for d in dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == expected + timedelta(days=1):
            continue
        else:
            break

    return streak


def best_daily_streak(habit_id: int) -> int:
    rows = habit_repo.get_habit_log_dates(habit_id, order="ASC")
    if not rows:
        return 0

    dates = [datetime.strptime(r, "%Y-%m-%d").date() for r in rows]
    best = 1
    current = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


# ════════════════════════════════════════════════════════════
# Weekly Streak
# ════════════════════════════════════════════════════════════

def weekly_streak(habit_id: int) -> int:
    target = habit_repo.get_habit_frequency_count(habit_id)
    if not target:
        return 0

    streak = 0
    today = date.today()

    for week_offset in range(52):
        ws = start_of_week(today) - timedelta(weeks=week_offset)
        we = min(end_of_week(ws), today) if week_offset == 0 else end_of_week(ws)
        done = habit_repo.count_logs_in_range(habit_id, ws.isoformat(), we.isoformat())

        if done >= target:
            streak += 1
        elif week_offset == 0:
            continue
        else:
            break

    return streak


def best_weekly_streak(habit_id: int) -> int:
    target = habit_repo.get_habit_frequency_count(habit_id)
    if not target:
        return 0

    created_at = habit_repo.get_habit_created_at(habit_id)
    try:
        start_date = datetime.strptime(created_at, "%Y-%m-%d").date() if created_at else date.today() - timedelta(weeks=52)
    except ValueError:
        start_date = date.today() - timedelta(weeks=52)

    today = date.today()
    best = 0
    current = 0
    ws = start_of_week(start_date)

    while ws <= today:
        we = min(end_of_week(ws), today)
        done = habit_repo.count_logs_in_range(habit_id, ws.isoformat(), we.isoformat())

        if done >= target:
            current += 1
            best = max(best, current)
        else:
            current = 0

        ws += timedelta(weeks=1)

    return best


# ════════════════════════════════════════════════════════════
# وضعیت هفته جاری
# ════════════════════════════════════════════════════════════

def week_status(habit_id: int) -> dict:
    target = habit_repo.get_habit_frequency_count(habit_id)
    if not target:
        return {}

    today = date.today()
    ws = start_of_week(today)
    we = end_of_week(today)

    created_at = habit_repo.get_habit_created_at(habit_id)
    try:
        created_date = datetime.strptime(created_at, "%Y-%m-%d").date() if created_at else ws
    except ValueError:
        created_date = ws

    effective_start = max(ws, created_date)
    days_in_week_for_habit = (we - effective_start).days + 1
    effective_target = max(min(int(target), days_in_week_for_habit), 1)
    days_passed = max((today - effective_start).days, 0)

    done = habit_repo.count_logs_in_range(habit_id, effective_start.isoformat(), today.isoformat())

    log_dates = set(habit_repo.get_habit_log_dates(
        habit_id, start_date=ws.isoformat(), end_date=we.isoformat()
    ))

    daily_log = [
        (ws + timedelta(days=i)).isoformat() in log_dates
        for i in range(7)
    ]
    remaining = max(effective_target - done, 0)
    days_left = (we - today).days + 1
    pct = round(done / effective_target * 100) if effective_target else 0
    on_track = days_left >= remaining

    return {
        "done":             done,
        "target":           target,
        "effective_target": effective_target,
        "remaining":        remaining,
        "pct":              pct,
        "on_track":         on_track,
        "days_left":        days_left,
        "days_passed":      days_passed,
        "daily_log":        daily_log,
    }

# ════════════════════════════════════════════════════════════
# گزارش همه عادت‌ها
# ════════════════════════════════════════════════════════════

def all_habits_report() -> list:
    habits = habit_repo.get_all_habits()
    report = []

    for h in habits:
        ws = week_status(h.id)
        report.append({
            "habit":          h,
            "daily_streak":   daily_streak(h.id),
            "best_streak":    best_daily_streak(h.id),
            "weekly_streak":  weekly_streak(h.id),
            "week_status":    ws,
            "done_today":     habit_repo.is_habit_done_today(h.id),
            "prediction":     predict_streak_break(h.id),
        })

    return report


# ════════════════════════════════════════════════════════════
# پیش‌بینی
# ════════════════════════════════════════════════════════════

def predict_streak_break(habit_id: int) -> str:
    status = week_status(habit_id)
    if not status:
        return "unknown"

    if status["remaining"] == 0:
        return "on_track"

    # اگه حتی با انجام کامل روزهای باقی‌مونده هم نشه به هدف رسید
    if status["days_left"] < status["remaining"]:
        return "broken"

    # عقب بودن از برنامه یعنی روزهای قبل از امروز رو از دست دادی
    days_passed = status.get("days_passed", 0)
    if status["done"] < days_passed:
        return "at_risk"

    return "on_track"
