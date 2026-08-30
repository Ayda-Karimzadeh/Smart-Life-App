"""
core/streak_engine.py
─────────────────────────────────────────────────────────────
منطق محاسبه Streak برای عادت‌های روزانه و هفتگی.

کاملاً مستقل از UI.
فقط از repository داده می‌گیرد و نتیجه برمی‌گرداند.
"""

from datetime import date, timedelta, datetime

from database.repository import habit_repo
from core.dates import start_of_week, end_of_week


# ════════════════════════════════════════════════════════════
# تنظیمات وضعیت هفتگی
# ════════════════════════════════════════════════════════════

# اگر برای رسیدن به هدف فقط به اندازه این تعداد روز
# حاشیه امن باقی مانده باشد، عادت at_risk محسوب می‌شود.
#
# مثال:
# هدف = 3
# باقی‌مانده = 3
# روزهای باقی‌مانده = 4
# حاشیه امن = 1
# => at_risk
#
# این مقدار را می‌توان بعداً بر اساس UX تغییر داد.
RISK_BUFFER_DAYS = 1


# ════════════════════════════════════════════════════════════
# Daily Streak
# ════════════════════════════════════════════════════════════

def daily_streak(habit_id: int) -> int:
    """Current streak only counts consecutive completions through today.

    If today is not completed, the current streak is considered broken and returns 0.
    """
    rows = habit_repo.get_habit_log_dates(
        habit_id,
        order="DESC"
    )

    if not rows:
        return 0

    dates = [
        datetime.strptime(r, "%Y-%m-%d").date()
        for r in rows
    ]

    today = date.today()
    if dates[0] != today:
        return 0

    streak = 1
    expected = today - timedelta(days=1)

    for d in dates[1:]:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    return streak


def best_daily_streak(habit_id: int) -> int:
    rows = habit_repo.get_habit_log_dates(
        habit_id,
        order="ASC"
    )

    if not rows:
        return 0

    dates = [
        datetime.strptime(r, "%Y-%m-%d").date()
        for r in rows
    ]

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
    """
    تعداد هفته‌های متوالی که عادت به هدف هفتگی رسیده است.

    هفته جاری اگر هنوز کامل نشده باشد، streak را نمی‌شکند.
    """

    target = habit_repo.get_habit_frequency_count(habit_id)

    if not target:
        return 0

    streak = 0
    today = date.today()

    for week_offset in range(52):
        ws = start_of_week(today) - timedelta(weeks=week_offset)

        if week_offset == 0:
            we = min(end_of_week(ws), today)
        else:
            we = end_of_week(ws)

        done = habit_repo.count_logs_in_range(
            habit_id,
            ws.isoformat(),
            we.isoformat()
        )

        if done >= target:
            streak += 1

        elif week_offset == 0:
            # هفته جاری هنوز تمام نشده است.
            # شکست محسوب نمی‌شود.
            continue

        else:
            break

    return streak


def best_weekly_streak(habit_id: int) -> int:
    """
    بهترین تعداد هفته‌های متوالی که عادت به هدف هفتگی رسیده است.
    هفته جاری، اگر هنوز کامل نشده باشد، در شمارش streak وارد نمی‌شود.
    """

    target = habit_repo.get_habit_frequency_count(habit_id)

    if not target:
        return 0

    created_at = habit_repo.get_habit_created_at(habit_id)

    try:
        start_date = (
            datetime.strptime(created_at, "%Y-%m-%d").date()
            if created_at
            else date.today() - timedelta(weeks=52)
        )
    except ValueError:
        start_date = date.today() - timedelta(weeks=52)

    today = date.today()

    best = 0
    current = 0

    ws = start_of_week(start_date)

    while ws < start_of_week(today):
        we = end_of_week(ws)

        done = habit_repo.count_logs_in_range(
            habit_id,
            ws.isoformat(),
            we.isoformat()
        )

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
    """
    وضعیت عادت در هفته جاری.

    خروجی شامل:
        done
        target
        effective_target
        remaining
        pct
        on_track
        days_left
        days_passed
        daily_log
    """

    target = habit_repo.get_habit_frequency_count(habit_id)

    if not target:
        return {}

    today = date.today()

    ws = start_of_week(today)
    we = end_of_week(today)

    # ────────────────────────────────────────────────────────
    # تاریخ ایجاد عادت
    # ────────────────────────────────────────────────────────

    created_at = habit_repo.get_habit_created_at(habit_id)

    try:
        created_date = (
            datetime.strptime(created_at, "%Y-%m-%d").date()
            if created_at
            else ws
        )
    except ValueError:
        created_date = ws

    # اگر عادت قبل از شروع هفته ساخته شده باشد،
    # محاسبه از ابتدای هفته انجام می‌شود.
    #
    # اگر وسط هفته ساخته شده باشد،
    # فقط روزهای بعد از ایجاد عادت در نظر گرفته می‌شوند.
    effective_start = max(ws, created_date)

    # اگر عادت از امروز یا قبل‌تر ساخته شده باشد،
    # تعداد روزهای قابل استفاده در این هفته:
    days_in_week_for_habit = max(
        (we - effective_start).days + 1,
        1
    )

    # ────────────────────────────────────────────────────────
    # هدف مؤثر این هفته
    # ────────────────────────────────────────────────────────

    effective_target = max(
        min(int(target), days_in_week_for_habit),
        1
    )

    # اگر target از مرز هفته بیشتر باشد، اینجا به‌صورت صریحی محدود می‌شود.
    # Validation واقعی باید در layer ورودی/Repository انجام شود، اما برای وضعیت فعلی
    # UI نباید مقدار غیرمنطقی را از این helper دریافت کند.
    if target > days_in_week_for_habit:
        effective_target = days_in_week_for_habit

    # ────────────────────────────────────────────────────────
    # تعداد روزهای سپری‌شده
    # ────────────────────────────────────────────────────────
    #
    # +1 یعنی امروز هم یک فرصت محسوب می‌شود.
    #
    # مثال:
    # شنبه -> 1
    # یکشنبه -> 2
    # دوشنبه -> 3
    #
    elapsed_days = max(
        (today - effective_start).days + 1,
        1
    )

    elapsed_days = min(
        elapsed_days,
        days_in_week_for_habit
    )

    # ────────────────────────────────────────────────────────
    # تعداد دفعات انجام‌شده
    # ────────────────────────────────────────────────────────

    done = habit_repo.count_logs_in_range(
        habit_id,
        effective_start.isoformat(),
        today.isoformat()
    )

    done_for_status = min(done, effective_target)
    done_value = done_for_status

    # ────────────────────────────────────────────────────────
    # باقی‌مانده
    # ────────────────────────────────────────────────────────

    remaining = max(
        effective_target - done_for_status,
        0
    )

    # ────────────────────────────────────────────────────────
    # روزهای باقی‌مانده
    # ────────────────────────────────────────────────────────

    days_left = max(
        (we - today).days + 1,
        0
    )

    # اگر عادت بعد از امروز ساخته شده باشد،
    # نباید days_left منفی یا غیرواقعی شود.
    if effective_start > today:
        days_left = 0

    # ────────────────────────────────────────────────────────
    # درصد پیشرفت
    # ────────────────────────────────────────────────────────

    pct = (
        round(done_for_status / effective_target * 100)
        if effective_target
        else 0
    )

    # درصد را محدود می‌کنیم.
    pct = min(max(pct, 0), 100)

    # ────────────────────────────────────────────────────────
    # منطق وضعیت
    # ────────────────────────────────────────────────────────
    #
    # remaining:
    # چند بار دیگر باید انجام شود؟
    #
    # days_left:
    # چند روز فرصت باقی مانده؟
    #
    # اگر:
    #
    # days_left < remaining
    #
    # حتی با انجام تمام روزهای باقی‌مانده هم
    # رسیدن به هدف ممکن نیست.
    #
    # => broken
    #
    # در غیر این صورت:
    #
    # slack = days_left - remaining
    #
    # slack نشان می‌دهد چند روز "حاشیه امن" داریم.
    #
    # مثال:
    #
    # target = 3
    # done = 0
    # days_left = 6
    #
    # remaining = 3
    # slack = 3
    #
    # => on_track
    #
    # اگر:
    #
    # remaining = 3
    # days_left = 4
    #
    # slack = 1
    #
    # => at_risk
    # ────────────────────────────────────────────────────────

    if remaining == 0:
        status = "on_track"

    elif days_left < remaining:
        status = "broken"

    else:
        slack = days_left - remaining

        if slack <= RISK_BUFFER_DAYS:
            status = "at_risk"
        else:
            status = "on_track"

    # ────────────────────────────────────────────────────────
    # وضعیت منطقی ساده برای مصرف UI
    # ────────────────────────────────────────────────────────

    on_track = status == "on_track"

    # ────────────────────────────────────────────────────────
    # لاگ‌های روزانه هفته
    # ────────────────────────────────────────────────────────

    log_dates = set(
        habit_repo.get_habit_log_dates(
            habit_id,
            start_date=ws.isoformat(),
            end_date=we.isoformat()
        )
    )

    daily_log = [
        (ws + timedelta(days=i)).isoformat() in log_dates
        for i in range(7)
    ]

    return {
        "done": done_value,
        "target": target,
        "effective_target": effective_target,
        "remaining": remaining,
        "pct": pct,
        "status": status,
        "on_track": on_track,
        "days_left": days_left,
        "days_passed": elapsed_days,
        "daily_log": daily_log,
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
            "habit": h,
            "daily_streak": daily_streak(h.id),
            "best_streak": best_daily_streak(h.id),
            "weekly_streak": weekly_streak(h.id),
            "week_status": ws,
            "done_today": habit_repo.is_habit_done_today(h.id),
            "prediction": predict_streak_break(h.id),
        })

    return report


# ════════════════════════════════════════════════════════════
# پیش‌بینی وضعیت Streak
# ════════════════════════════════════════════════════════════

def predict_streak_break(habit_id: int) -> str:
    """
    پیش‌بینی وضعیت فعلی عادت هفتگی.

    خروجی:
        on_track
        at_risk
        broken
        unknown
    """

    status = week_status(habit_id)

    if not status:
        return "unknown"

    return status.get("status", "unknown")