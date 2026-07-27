from datetime import date, datetime
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QScrollArea, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPolygonF, QPainterPath

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
    settings_repo,
)
from core.language_manager import tr


# ─── نمودار دایره‌ای ──────────────────────────────────────────────────────────
class CircleChart(QWidget):
    def __init__(self, value=0, color=ACCENT2, parent=None):
        super().__init__(parent)
        self.value = value
        self.color = color
        self.setFixedSize(130, 130)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = min(self.width(), self.height()) - 16
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        p.setPen(QPen(QColor(BG_CARD2), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(x, y, size, size, 0, 360 * 16)
        span = int(self.value / 100 * 360 * 16)
        p.setPen(QPen(QColor(self.color), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(x, y, size, size, 90 * 16, -span)
        p.setPen(QColor(TEXT_PRIMARY))
        p.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.value}%")


# ─── نمودار خطی ──────────────────────────────────────────────────────────────
class LineChart(QWidget):
    def __init__(self, data=None, color=ACCENT2, parent=None):
        super().__init__(parent)
        self.data = data or [0] * 7
        self.color = color
        self.setMinimumHeight(120)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        pad = 10
        mn, mx = min(self.data), max(self.data)
        rang = mx - mn if mx != mn else 1
        pts = []
        for i, v in enumerate(self.data):
            x = pad + i * (w - 2 * pad) / max(len(self.data) - 1, 1)
            y = h - pad - (v - mn) / rang * (h - 2 * pad)
            pts.append((x, y))
        fill_color = QColor(self.color)
        fill_color.setAlpha(40)
        p.setBrush(QBrush(fill_color))
        p.setPen(Qt.PenStyle.NoPen)
        poly_pts = [(pad, h - pad)] + pts + [(w - pad, h - pad)]
        poly = QPolygonF([QPointF(x, y) for x, y in poly_pts])
        p.drawPolygon(poly)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(self.color), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        path = QPainterPath()
        path.moveTo(pts[0][0], pts[0][1])
        for x, y in pts[1:]:
            path.lineTo(x, y)
        p.drawPath(path)


def _greeting():
    h = datetime.now().hour
    if h < 12:   return "Good morning"
    elif h < 17: return "Good afternoon"
    else:        return "Good evening"

def _fmt_time(secs):
    h = int(secs // 3600)
    m = int((secs % 3600) // 60)
    return f"{h}h {m}m" if h else f"{m}m"


def _needs_getting_started() -> bool:
    """هنوز هیچ فعالیتی ثبت نشده — به‌جای درصد صفر، راهنمای شروع نشون بده."""
    habits = habit_repo.get_all_habits()
    goals = goal_repo.get_all_goals()
    tasks = task_repo.get_all_tasks()
    
    # If user has data but no activity yet, show getting started
    has_data = habits or goals or tasks
    has_activity = analytics_repo.has_any_habit_logs() or analytics_repo.has_any_time_sessions()
    
    return has_data and not has_activity


def _display_name() -> str:
    name = settings_repo.get_user_name().strip()
    return name or "there"


# ─── صفحه: Dashboard ─────────────────────────────────────────────────────────
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.refresh()

    def refresh(self):
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)
        
        habits = habit_repo.get_all_habits()
        goals = goal_repo.get_all_goals()
        tasks = task_repo.get_all_tasks()
        has_any_data = habits or goals or tasks
        
        if not has_any_data:
            layout.addWidget(self._empty_state())
        else:
            layout.addWidget(self._banner())
            if _needs_getting_started():
                layout.addWidget(self._getting_started())
                layout.addWidget(self._today_habits())
            else:
                layout.addWidget(self._stats_row())
                layout.addWidget(self._charts_row())
                layout.addWidget(self._habit_streaks())
            layout.addWidget(self._tasks_goals_row())
        
        layout.addStretch()
        self.scroll.setWidget(content)

    # ─ Empty State ─────────────────────────────────────────────────────────────
    def _empty_state(self):
        empty_container = QWidget()
        empty_container.setStyleSheet("background: transparent;")
        empty_lay = QVBoxLayout(empty_container)
        empty_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_lay.setSpacing(16)
        empty_lay.setContentsMargins(40, 100, 40, 100)

        icon = QLabel("🏠")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 72px; background: transparent;")
        empty_lay.addWidget(icon)

        title = QLabel(tr("welcome"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 24px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        empty_lay.addWidget(title)

        desc = QLabel(tr("onboarding_desc"))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        desc.setWordWrap(True)
        empty_lay.addWidget(desc)

        return empty_container

    # ─ بنر ───────────────────────────────────────────────────────────────────
    def _banner(self):
        habits = habit_repo.get_all_habits()
        max_streak = max((habit_repo.get_current_streak(h.id) for h in habits), default=0) if habits else 0
        level = max(1, max_streak // 5)
        name = _display_name()
        getting_started = _needs_getting_started()

        card = make_card(color="#1a1530")
        card.setMinimumHeight(150)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 22, 28, 22)
        lay.setSpacing(10)

        if getting_started:
            title = QLabel(f"{_greeting()}, {name} ✨")
            sub = QLabel(
                "خوش اومدی! عادت‌هات آماده‌ان — "
                "اولین‌هاشون رو تیک بزن تا پیشرفتت اینجا دیده بشه."
            )
        elif max_streak > 0:
            title = QLabel(f"{_greeting()}, {name} ✨")
            sub = QLabel("You're doing amazing! Keep pushing forward on your journey to greatness.")
        else:
            title = QLabel(f"{_greeting()}, {name} ✨")
            sub = QLabel("Every small step counts. Mark a habit done today to start your streak.")

        title.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")

        badges = QHBoxLayout()
        if getting_started:
            badge_items = [
                ("🌱", f"{len(habits)} habits ready", GREEN),
                ("🎯", "Let's begin", ACCENT2),
            ]
        else:
            badge_items = [
                ("🔥", f"{max_streak} day streak", ORANGE),
                ("🏆", f"Level {level} Achiever", ACCENT2),
            ]

        for icon, txt, col in badge_items:
            btn = QPushButton(f"  {icon}  {txt}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255,255,255,0.07);
                    color: {col};
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 18px; padding: 6px 16px;
                    font-size: 13px; font-weight: 600;
                }}
            """)
            badges.addWidget(btn)
        badges.addStretch()
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addLayout(badges)
        return card

    def _getting_started(self):
        card = make_card(color="#1a2530")
        card.setMinimumHeight(140)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        title = QLabel("🚀  Getting Started")
        title.setStyleSheet(f"font-size: 17px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        steps = [
            ("1", "Go to Habits and check off what you did today"),
            ("2", "Add a task or start a focus timer"),
            ("3", "Come back here — your stats will fill in automatically"),
        ]
        for num, text in steps:
            row = QHBoxLayout()
            num_lbl = QLabel(num)
            num_lbl.setFixedSize(26, 26)
            num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_lbl.setStyleSheet(f"""
                background: rgba(124,92,191,0.35); color: {ACCENT2};
                border-radius: 13px; font-size: 12px; font-weight: bold;
            """)
            txt_lbl = QLabel(text)
            txt_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
            row.addWidget(num_lbl)
            row.addWidget(txt_lbl, 1)
            lay.addLayout(row)

        return card

    def _today_habits(self):
        habits = habit_repo.get_all_habits()

        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        title = QLabel("Today's Habits")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        hint = QLabel("Tap a habit in the Habits page to mark it done")
        hint.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(title)
        lay.addWidget(hint)

        if not habits:
            empty = QLabel(tr("no_habits_yet"))
            empty.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent; padding: 8px 0;")
            lay.addWidget(empty)
            return section

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(14)

        for h in habits[:4]:
            done = habit_repo.is_habit_done_today(h.id)
            card = make_card(color="#1a2a1a" if done else BG_CARD2)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(6)

            top = QHBoxLayout()
            icon_lbl = QLabel(h.icon)
            icon_lbl.setStyleSheet("font-size: 22px; background: transparent;")
            status = QLabel("Done" if done else "Pending")
            status.setStyleSheet(
                f"font-size: 11px; font-weight: 600; color: {GREEN if done else TEXT_MUTED}; background: transparent;"
            )
            top.addWidget(icon_lbl)
            top.addStretch()
            top.addWidget(status)

            n = QLabel(h.name)
            n.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
            cl.addLayout(top)
            cl.addWidget(n)
            rl.addWidget(card)

        for _ in range(max(0, 4 - len(habits[:4]))):
            rl.addStretch(1)

        lay.addWidget(row)
        return section

    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        # داده‌های واقعی
        habits = habit_repo.get_all_habits()
        total_habits = len(habits)
        done_today   = sum(1 for h in habits if habit_repo.is_habit_done_today(h.id))

        goals        = goal_repo.get_all_goals()
        active_goals = len(goals)

        focus_today  = analytics_repo.get_total_time_today()

        if total_habits > 0:
            daily_pct = round(done_today / total_habits * 100)
        else:
            daily_pct = 0

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("📈", f"{daily_pct}%",
             "Daily Progress",   "Habit completion today", GREEN,  ""),
            ("✅", f"{done_today}/{total_habits}",
             "Habits Completed", "Keep it up!",            GREEN,  ""),
            ("🎯", str(active_goals),
             "Active Goals",     "In progress",            BLUE,   ""),
            ("⏱",  _fmt_time(focus_today),
             "Focus Time Today", "Tracked sessions",       ORANGE, ""),
        ]

        for icon, val, title, sub, col, badge in items:
            card = make_card()
            card.setMinimumHeight(130)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(4)
            top = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px; padding: 6px;")
            icon_lbl.setFixedSize(40, 40)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            top.addWidget(icon_lbl)
            top.addStretch()
            val_lbl = QLabel(val)
            val_lbl.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_PRIMARY}; background: transparent; font-weight: 500;")
            s_lbl = QLabel(sub)
            s_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            cl.addLayout(top)
            cl.addWidget(val_lbl)
            cl.addWidget(t_lbl)
            cl.addWidget(s_lbl)
            lay.addWidget(card)
        return row

    # ─ نمودارها ──────────────────────────────────────────────────────────────
    def _charts_row(self):
        habits = habit_repo.get_all_habits()
        total  = len(habits)

        # Daily Score — درصد انجام امروز
        done_today = sum(1 for h in habits if habit_repo.is_habit_done_today(h.id))
        daily_score = round(done_today / total * 100) if total else 0

        # Weekly Avg — میانگین هفته جاری
        if habits:
            week_pcts = [
                min(habit_repo.get_week_progress(h.id) / h.frequency_count, 1) * 100
                for h in habits
            ]
            weekly_avg = round(sum(week_pcts) / len(week_pcts))
        else:
            weekly_avg = 0

        # نمودار خطی هفتگی از time_sessions
        weekly_data = analytics_repo.get_weekly_activity()
        chart_data  = [v for _, v in weekly_data]

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Today's Overview
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        title_lbl = QLabel("Today's Overview")
        title_lbl.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(title_lbl)
        circles = QHBoxLayout()
        for val, lbl, col in [(daily_score, "Daily Score", ACCENT2), (weekly_avg, "Weekly Avg", BLUE)]:
            vbox = QVBoxLayout()
            vbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            c = CircleChart(val, col)
            lbl_w = QLabel(lbl)
            lbl_w.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            lbl_w.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            vbox.addWidget(c)
            vbox.addWidget(lbl_w)
            circles.addLayout(vbox)
        ll.addLayout(circles)
        left.setMinimumWidth(280)

        # Weekly Activity
        right = make_card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(20, 18, 20, 18)
        rl.setSpacing(12)
        rtop = QHBoxLayout()
        t2 = QLabel("Weekly Activity")
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ps = QLabel("Focus Hours")
        ps.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        rtop.addWidget(t2)
        rtop.addStretch()
        rtop.addWidget(ps)
        chart = LineChart(data=chart_data, color=ACCENT2)
        chart.setMinimumHeight(160)
        rl.addLayout(rtop)
        rl.addWidget(chart)

        lay.addWidget(left, 1)
        lay.addWidget(right, 2)
        return row

    # ─ Tasks + Goals ──────────────────────────────────────────────────────────
    def _tasks_goals_row(self):
        today = date.today().isoformat()
        tasks_today = [t for t in task_repo.get_all_tasks() if t.due_date == today]
        goals       = goal_repo.get_all_goals()[:3]  # فقط ۳ تا

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Today's Tasks
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        header = QHBoxLayout()
        t = QLabel("Today's Tasks")
        t.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        header.addWidget(t)
        header.addStretch()
        ll.addLayout(header)

        if not tasks_today:
            empty = QLabel(tr("no_tasks_today"))
            empty.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            ll.addWidget(empty)
        else:
            for task in tasks_today[:4]:
                card = make_card(color="#1a2a1a" if task.done else BG_CARD2)
                cl = QHBoxLayout(card)
                cl.setContentsMargins(14, 10, 14, 10)
                cl.setSpacing(12)
                check = QLabel("●")
                check.setStyleSheet(f"font-size: 18px; color: {GREEN if task.done else TEXT_MUTED}; background: transparent;")
                check.setFixedWidth(22)
                info = QVBoxLayout()
                info.setSpacing(2)
                name_lbl = QLabel(task.name)
                name_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED if task.done else TEXT_PRIMARY}; background: transparent; {'text-decoration: line-through;' if task.done else ''}")
                time_lbl = QLabel(task.due_time or "")
                time_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
                info.addWidget(name_lbl)
                if task.due_time:
                    info.addWidget(time_lbl)
                cl.addWidget(check)
                cl.addLayout(info, 1)
                ll.addWidget(card)

        # Active Goals
        right = make_card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(20, 18, 20, 18)
        rl.setSpacing(12)
        rheader = QHBoxLayout()
        t2 = QLabel("Active Goals")
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        view_all = QLabel("View All →")
        view_all.setStyleSheet(f"font-size: 12px; color: {ACCENT2}; background: transparent;")
        rheader.addWidget(t2)
        rheader.addStretch()
        rheader.addWidget(view_all)
        rl.addLayout(rheader)

        COLORS = [ACCENT2, BLUE, ACCENT, GREEN, ORANGE]

        if not goals:
            empty = QLabel(tr("no_goals_yet"))
            empty.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            rl.addWidget(empty)
        else:
            for i, goal in enumerate(goals):
                pct = goal_repo.get_goal_progress_percent(goal.id)
                col = COLORS[i % len(COLORS)]
                gc = make_card(color=BG_CARD2)
                gl = QVBoxLayout(gc)
                gl.setContentsMargins(14, 12, 14, 12)
                gl.setSpacing(6)
                top = QHBoxLayout()
                n = QLabel(f"{goal.icon} {goal.name}")
                n.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
                p = QLabel(f"{pct}%")
                p.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {col}; background: transparent;")
                top.addWidget(n, 1)
                top.addWidget(p)
                cat_lbl = QLabel(goal.category)
                cat_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
                bar = QProgressBar()
                bar.setRange(0, 100)
                bar.setValue(pct)
                bar.setTextVisible(False)
                bar.setFixedHeight(6)
                bar.setStyleSheet(f"QProgressBar {{ background: {BG_CARD}; border-radius: 3px; }} QProgressBar::chunk {{ background: {col}; border-radius: 3px; }}")
                gl.addLayout(top)
                gl.addWidget(cat_lbl)
                gl.addWidget(bar)
                rl.addWidget(gc)

        rl.addStretch()
        lay.addWidget(left, 1)
        lay.addWidget(right, 1)
        return row

    # ─ Habit Streaks ─────────────────────────────────────────────────────────
    def _habit_streaks(self):
        habits = habit_repo.get_all_habits()

        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        title = QLabel("Habit Streaks")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        if not habits:
            empty = QLabel(tr("no_habits_add"))
            empty.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            lay.addWidget(empty)
            return section

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(14)

        # فقط ۴ تا نشون بده
        for h in habits[:4]:
            streak = habit_repo.get_current_streak(h.id)
            done   = habit_repo.is_habit_done_today(h.id)
            col    = ORANGE if streak > 0 else TEXT_MUTED

            card = make_card(color="#2a1a0a" if done else BG_CARD2)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(6)

            top = QHBoxLayout()
            fire = QLabel("🔥" if done else "🩶")
            fire.setStyleSheet("font-size: 18px; background: transparent;")
            days_lbl = QLabel(f"{streak} days")
            days_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {col}; background: transparent;")
            top.addWidget(fire)
            top.addStretch()
            top.addWidget(days_lbl)

            n = QLabel(h.name)
            n.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
            status = QLabel("Completed today" if done else "Not completed yet")
            status.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

            cl.addLayout(top)
            cl.addWidget(n)
            cl.addWidget(status)
            rl.addWidget(card)

        # اگه عادت‌ها کمتر از ۴ تا باشه، فضای خالی پر کن
        for _ in range(max(0, 4 - len(habits[:4]))):
            rl.addStretch(1)

        lay.addWidget(row)
        return section