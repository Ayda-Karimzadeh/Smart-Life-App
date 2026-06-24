"""
core/streak_engine.py
─────────────────────────────────────────────────────────────
منطق محاسبه Streak برای عادت‌های روزانه و هفتگی.
کاملاً مستقل از UI — فقط داده می‌گیره و عدد برمی‌گردونه.

تفاوت با db_manager.py:
  db_manager    → CRUD ساده (ثبت، خواندن، حذف)
  streak_engine → منطق پیچیده‌تر (weekly streak، پیش‌بینی، گزارش)
"""

from datetime import date, timedelta, datetime
from database import db_manager as db


# ════════════════════════════════════════════════════════════
# Daily Streak
# ════════════════════════════════════════════════════════════

def daily_streak(habit_id: int) -> int:
    """
    تعداد روزهای متوالی که یه عادت روزانه انجام شده.

    مثال:
      امروز ✅، دیروز ✅، پریروز ✅، ۳ روز قبل ❌  →  streak = 3
    """
    conn = db.get_connection()
    rows = conn.execute(
        "SELECT log_date FROM habit_logs WHERE habit_id = ? ORDER BY log_date DESC",
        (habit_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates    = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]
    streak   = 0
    expected = date.today()

    for d in dates:
        if d == expected:
            streak  += 1
            expected -= timedelta(days=1)
        elif d == expected + timedelta(days=1):
            # امروز هنوز انجام نشده ولی دیروز بوده
            continue
        else:
            break

    return streak


def best_daily_streak(habit_id: int) -> int:
    """طولانی‌ترین streak روزانه در کل تاریخچه."""
    conn = db.get_connection()
    rows = conn.execute(
        "SELECT log_date FROM habit_logs WHERE habit_id = ? ORDER BY log_date ASC",
        (habit_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates   = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]
    best    = 1
    current = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
            best     = max(best, current)
        else:
            current  = 1

    return best


# ════════════════════════════════════════════════════════════
# Weekly Streak (ویژگی اصلی پروژه)
# ════════════════════════════════════════════════════════════

def weekly_streak(habit_id: int) -> int:
    """
    تعداد هفته‌های متوالی که هدف frequency برآورده شده.

    مثال — عادت "ورزش ۳ بار در هفته":
      هفته جاری:   ۳ بار ✅  →  شمرده می‌شه
      هفته قبل:    ۳ بار ✅  →  streak = 2
      ۲ هفته قبل:  ۲ بار ❌  →  streak شکسته  →  نتیجه: 2
    """
    conn  = db.get_connection()
    habit = conn.execute(
        "SELECT frequency_count FROM habits WHERE id = ?",
        (habit_id,)
    ).fetchone()
    conn.close()

    if not habit:
        return 0

    target = habit[0]
    streak = 0
    today  = date.today()

    for week_offset in range(52):
        week_end   = today - timedelta(days=today.weekday() + week_offset * 7)
        week_start = week_end - timedelta(days=6)
        done       = _count_in_range(habit_id, week_start, week_end)

        if done >= target:
            streak += 1
        else:
            # هفته جاری ممکنه هنوز تموم نشده باشه
            if week_offset == 0:
                continue
            break

    return streak


def best_weekly_streak(habit_id: int) -> int:
    """طولانی‌ترین weekly streak در کل تاریخچه."""
    conn  = db.get_connection()
    habit = conn.execute(
        "SELECT frequency_count, created_at FROM habits WHERE id = ?",
        (habit_id,)
    ).fetchone()
    conn.close()

    if not habit:
        return 0

    target, created_at = habit[0], habit[1]

    try:
        start_date = datetime.strptime(created_at, "%Y-%m-%d").date()
    except Exception:
        start_date = date.today() - timedelta(weeks=52)

    today      = date.today()
    best       = 0
    current    = 0
    week_start = start_date - timedelta(days=start_date.weekday())

    while week_start <= today:
        week_end = week_start + timedelta(days=6)
        done     = _count_in_range(habit_id, week_start, min(week_end, today))

        if done >= target:
            current += 1
            best     = max(best, current)
        else:
            current  = 0

        week_start += timedelta(weeks=1)

    return best


# ════════════════════════════════════════════════════════════
# وضعیت هفته جاری
# ════════════════════════════════════════════════════════════

def week_status(habit_id: int) -> dict:
    """
    وضعیت کامل هفته جاری برای یه عادت.

    برمی‌گردونه:
    {
        "done":      3,                      # چند بار این هفته انجام شده
        "target":    5,                      # هدف هفتگی
        "remaining": 2,                      # چقدر مونده
        "pct":       60,                     # درصد پیشرفت
        "on_track":  True,                   # آیا در مسیر هدفه؟
        "days_left": 3,                      # روزهای باقیمانده هفته
        "daily_log": [T, F, T, F, F, F, F], # ۷ روز هفته
    }
    """
    conn  = db.get_connection()
    habit = conn.execute(
        "SELECT frequency_count FROM habits WHERE id = ?",
        (habit_id,)
    ).fetchone()
    conn.close()

    if not habit:
        return {}

    target     = habit[0]
    today      = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end   = week_start + timedelta(days=6)
    done       = _count_in_range(habit_id, week_start, today)

    conn       = db.get_connection()
    done_dates = {
        r[0] for r in conn.execute(
            "SELECT log_date FROM habit_logs WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
            (habit_id, week_start.isoformat(), week_end.isoformat())
        ).fetchall()
    }
    conn.close()

    daily_log  = [
        (week_start + timedelta(days=i)).isoformat() in done_dates
        for i in range(7)
    ]
    remaining  = max(target - done, 0)
    days_left  = (week_end - today).days + 1
    pct        = round(done / target * 100) if target else 0
    on_track   = days_left >= remaining

    return {
        "done":      done,
        "target":    target,
        "remaining": remaining,
        "pct":       pct,
        "on_track":  on_track,
        "days_left": days_left,
        "daily_log": daily_log,
    }


# ════════════════════════════════════════════════════════════
# گزارش همه عادت‌ها
# ════════════════════════════════════════════════════════════

def all_habits_report() -> list:
    """
    گزارش کامل همه عادت‌ها.

    برمی‌گردونه:
    [
        {
            "habit":         <Habit>,
            "daily_streak":  5,
            "best_streak":   12,
            "weekly_streak": 3,
            "week_status":   {...},
            "done_today":    True,
            "prediction":    "on_track",
        },
        ...
    ]
    """
    habits = db.get_all_habits()
    report = []

    for h in habits:
        ws = week_status(h.id)
        report.append({
            "habit":          h,
            "daily_streak":   daily_streak(h.id),
            "best_streak":    best_daily_streak(h.id),
            "weekly_streak":  weekly_streak(h.id),
            "week_status":    ws,
            "done_today":     db.is_habit_done_today(h.id),
            "prediction":     predict_streak_break(h.id),
        })

    return report


# ════════════════════════════════════════════════════════════
# پیش‌بینی
# ════════════════════════════════════════════════════════════

def predict_streak_break(habit_id: int) -> str:
    """
    پیش‌بینی وضعیت streak هفته جاری.

    برمی‌گردونه:
      "on_track"  — در مسیر هدف، راحت می‌رسه
      "at_risk"   — باید هر روز باقیمانده انجام بده
      "broken"    — دیگه این هفته امکان رسیدن به هدف نیست
    """
    status = week_status(habit_id)
    if not status:
        return "unknown"

    if status["remaining"] == 0:
        return "on_track"

    if status["days_left"] < status["remaining"]:
        return "broken"

    if status["days_left"] <= status["remaining"] + 1:
        return "at_risk"

    return "on_track"


# ════════════════════════════════════════════════════════════
# تابع کمکی
# ════════════════════════════════════════════════════════════

def _count_in_range(habit_id: int, start: date, end: date) -> int:
    """تعداد روزهای انجام‌شده بین دو تاریخ"""
    conn = db.get_connection()
    row  = conn.execute(
        "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
        (habit_id, start.isoformat(), end.isoformat())
    ).fetchone()
    conn.close()
    return row[0] if row else 0