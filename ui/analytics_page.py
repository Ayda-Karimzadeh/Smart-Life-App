import math
from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QFrame
)

from PyQt6.QtCore import Qt, QPointF

from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush,
    QPolygonF, QPainterPath, QFont
)

from assets.style import (
    BG_CARD, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)

from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
)
from core.dates import start_of_week, end_of_week


# ─── نمودار خطی با نقاط ──────────────────────────────────────────────────────
class LineChartDot(QWidget):
    def __init__(self, data=None, labels=None, color=ACCENT2, filled=False, parent=None):
        super().__init__(parent)
        self.data   = data   or [0]
        self.labels = labels or []
        self.color  = color
        self.filled = filled
        self.setMinimumHeight(180)

    def paintEvent(self, event):
        if not self.data or max(self.data) == 0:
            p = QPainter(self)
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 11))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No data yet")
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 30
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        mn, mx = 0, max(self.data) or 1

        pts = []
        for i, v in enumerate(self.data):
            x = pad_l + i * chart_w / max(len(self.data) - 1, 1)
            y = pad_t + chart_h - (v - mn) / (mx - mn) * chart_h
            pts.append((x, y))

        # خطوط راهنما
        for i in range(5):
            val = int(mx - i * mx / 4)
            y   = int(pad_t + i * chart_h / 4)
            p.setPen(QPen(QColor(50, 50, 70), 1))
            p.drawLine(pad_l, y, w - pad_r, y)
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, y - 6, pad_l - 4, 14, Qt.AlignmentFlag.AlignRight, str(val))

        # سطح پر
        if self.filled:
            fill = QColor(self.color)
            fill.setAlpha(30)
            p.setBrush(QBrush(fill))
            p.setPen(Qt.PenStyle.NoPen)
            poly = [(pad_l, pad_t + chart_h)] + pts + [(pts[-1][0], pad_t + chart_h)]
            p.drawPolygon(QPolygonF([QPointF(x, y) for x, y in poly]))

        # خط
        path = QPainterPath()
        path.moveTo(pts[0][0], pts[0][1])
        for x, y in pts[1:]:
            path.lineTo(x, y)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(self.color), 2.5,
                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawPath(path)

        # نقاط
        for x, y in pts:
            p.setBrush(QBrush(QColor(self.color)))
            p.setPen(QPen(QColor(BG_CARD), 2))
            p.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)

        # برچسب‌های محور X
        if self.labels:
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            for i, lbl in enumerate(self.labels):
                x = pad_l + i * chart_w / max(len(self.data) - 1, 1)
                p.drawText(int(x) - 15, h - pad_b + 6, 30, 20,
                           Qt.AlignmentFlag.AlignHCenter, lbl)


# ─── نمودار رادار ─────────────────────────────────────────────────────────────
class RadarChart(QWidget):
    def __init__(self, labels=None, values=None, parent=None):
        super().__init__(parent)
        self.labels = labels or ["Habits", "Goals", "Tasks", "Time", "Streak"]
        self.values = values or [0, 0, 0, 0, 0]
        self.setMinimumSize(250, 250)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width() // 2, self.height() // 2
        r = min(cx, cy) - 40
        n = len(self.values)

        # خطوط راهنما
        for level in [25, 50, 75, 100]:
            pts = []
            for i in range(n):
                angle = math.pi / 2 + 2 * math.pi * i / n
                rr = r * level / 100
                pts.append(QPointF(cx + rr * math.cos(angle), cy - rr * math.sin(angle)))
            p.setPen(QPen(QColor(60, 60, 80), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            for i in range(n):
                p.drawLine(pts[i], pts[(i + 1) % n])

        # محورها
        p.setPen(QPen(QColor(60, 60, 80), 1))
        for i in range(n):
            angle = math.pi / 2 + 2 * math.pi * i / n
            p.drawLine(int(cx), int(cy),
                       int(cx + r * math.cos(angle)),
                       int(cy - r * math.sin(angle)))

        # سطح داده
        pts = []
        for i, v in enumerate(self.values):
            angle = math.pi / 2 + 2 * math.pi * i / n
            rr = r * min(v, 100) / 100
            pts.append(QPointF(cx + rr * math.cos(angle), cy - rr * math.sin(angle)))

        fill = QColor(ACCENT)
        fill.setAlpha(60)
        p.setBrush(QBrush(fill))
        p.setPen(QPen(QColor(ACCENT2), 2))
        p.drawPolygon(QPolygonF(pts))

        for pt in pts:
            p.setBrush(QBrush(QColor(ACCENT2)))
            p.setPen(QPen(QColor(BG_CARD), 2))
            p.drawEllipse(pt, 5, 5)

        # برچسب‌ها
        p.setPen(QColor(TEXT_MUTED))
        p.setFont(QFont("Segoe UI", 9))
        for i, lbl in enumerate(self.labels):
            angle = math.pi / 2 + 2 * math.pi * i / n
            x = cx + (r + 18) * math.cos(angle)
            y = cy - (r + 18) * math.sin(angle)
            p.drawText(int(x) - 30, int(y) - 8, 60, 16,
                       Qt.AlignmentFlag.AlignHCenter, lbl)


# ─── نمودار میله‌ای مقایسه‌ای ─────────────────────────────────────────────────
class CompareBarChart(QWidget):
    def __init__(self, labels=None, this_week=None, last_week=None, parent=None):
        super().__init__(parent)
        self.labels    = labels    or ["Week 1", "Week 2", "Week 3", "Week 4"]
        self.this_week = this_week or [0, 0, 0, 0]
        self.last_week = last_week or [0, 0, 0, 0]
        self.setMinimumHeight(220)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 40
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        all_vals = self.this_week + self.last_week
        max_val  = max(all_vals) if any(all_vals) else 1

        n       = len(self.labels)
        group_w = chart_w / n
        bar_w   = int(group_w * 0.28)
        gap     = 4

        # خطوط راهنما
        for i in range(5):
            val = int(max_val - i * max_val / 4)
            y   = int(pad_t + i * chart_h / 4)
            p.setPen(QPen(QColor(50, 50, 70), 1))
            p.drawLine(pad_l, y, w - pad_r, y)
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, y - 6, pad_l - 4, 14, Qt.AlignmentFlag.AlignRight, str(val))

        for i, (lv, tv) in enumerate(zip(self.last_week, self.this_week)):
            gx = pad_l + i * group_w + group_w / 2

            bh = int(lv / max_val * chart_h) if max_val else 0
            x1 = int(gx - bar_w - gap / 2)
            p.setBrush(QBrush(QColor(100, 100, 130)))
            p.setPen(Qt.PenStyle.NoPen)
            if bh:
                p.drawRoundedRect(x1, pad_t + chart_h - bh, bar_w, bh, 4, 4)

            bh2 = int(tv / max_val * chart_h) if max_val else 0
            x2  = int(gx + gap / 2)
            p.setBrush(QBrush(QColor(ACCENT2)))
            if bh2:
                p.drawRoundedRect(x2, pad_t + chart_h - bh2, bar_w, bh2, 4, 4)

            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(int(gx) - 25, h - pad_b + 6, 50, 20,
                       Qt.AlignmentFlag.AlignHCenter, self.labels[i])

        # legend
        p.setFont(QFont("Segoe UI", 10))
        lx, ly = pad_l + 10, h - 18
        p.setBrush(QBrush(QColor(100, 100, 130)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(lx, ly, 12, 12)
        p.setPen(QColor(TEXT_MUTED))
        p.drawText(lx + 16, ly - 1, 80, 14, Qt.AlignmentFlag.AlignLeft, "Last Week")
        lx2 = lx + 110
        p.setBrush(QBrush(QColor(ACCENT2)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(lx2, ly, 12, 12)
        p.setPen(QColor(ACCENT2))
        p.drawText(lx2 + 16, ly - 1, 80, 14, Qt.AlignmentFlag.AlignLeft, "This Week")


# ─── صفحه: Analytics ─────────────────────────────────────────────────────────
class AnalyticsPage(QWidget):
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
        # ─ بارگذاری همه داده‌ها یک‌بار ─
        self._habits     = habit_repo.get_all_habits()
        self._goals      = goal_repo.get_all_goals()
        self._tasks      = task_repo.get_all_tasks()
        self._weekly     = analytics_repo.get_weekly_activity()
        self._dist       = analytics_repo.get_time_distribution()
        self._focus_today = analytics_repo.get_total_time_today()

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        layout.addWidget(self._stats_row())

        insights = self._insights()
        if insights:
            layout.addWidget(insights)

        layout.addWidget(self._trend_charts())

        if self._habits or self._tasks:
            layout.addWidget(self._radar_compare_row())

        layout.addWidget(self._performance_banner())
        layout.addStretch()

        self.scroll.setWidget(content)

    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        habits      = self._habits
        total       = len(habits)
        done_today  = sum(1 for h in habits if habit_repo.is_habit_done_today(h.id))
        habit_pct   = round(done_today / total * 100) if total else 0

        goals       = self._goals
        goal_progs  = [goal_repo.get_goal_progress_percent(g.id) for g in goals]
        avg_goal    = round(sum(goal_progs) / len(goal_progs)) if goal_progs else 0

        tasks       = self._tasks
        done_tasks  = sum(1 for t in tasks if t.done)
        task_pct    = round(done_tasks / len(tasks) * 100) if tasks else 0

        max_streak  = max((habit_repo.get_current_streak(h.id) for h in habits), default=0)

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("📈", str(habit_pct) + "%", "Habit Score",       "Today's completion",  ACCENT2, True,  f"+{habit_pct}%", GREEN),
            ("💚", str(avg_goal)  + "%", "Goal Progress",     "Average across goals", GREEN,   False, f"{avg_goal}%",  GREEN),
            ("✅", str(task_pct)  + "%", "Task Completion",   "All time",            BLUE,    False, f"{task_pct}%",  BLUE),
            ("🔥", str(max_streak),      "Longest Streak",    "Days active",         ORANGE,  False, "Best" if max_streak > 0 else "—", ORANGE),
        ]

        for icon, val, title, sub, col, highlight, badge, badge_col in items:
            card = make_card(color="#1a1535" if highlight else BG_CARD)
            card.setMinimumHeight(140)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(18, 16, 18, 16)
            cl.setSpacing(6)
            top = QHBoxLayout()
            icon_box = QLabel(icon)
            icon_box.setFixedSize(40, 40)
            icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_box.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px;")
            badge_lbl = QLabel(badge)
            badge_lbl.setStyleSheet(f"font-size: 12px; color: {badge_col}; background: transparent; font-weight: 600;")
            top.addWidget(icon_box)
            top.addStretch()
            top.addWidget(badge_lbl)
            val_lbl = QLabel(val)
            val_lbl.setStyleSheet(f"font-size: 30px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
            s_lbl = QLabel(sub)
            s_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            cl.addLayout(top)
            cl.addWidget(val_lbl)
            cl.addWidget(t_lbl)
            cl.addWidget(s_lbl)
            lay.addWidget(card)

        return row

    # ─ Key Insights ──────────────────────────────────────────────────────────
    def _insights(self):
        insights = []

        # Streak بالا
        for h in self._habits:
            streak = habit_repo.get_current_streak(h.id)
            if streak >= 7:
                insights.append(("🔥", f"{streak}-Day Streak!",
                                  f"You've kept up '{h.name}' for {streak} days. Amazing!",
                                  "#2a1a0a", ORANGE))
                break

        # هدف نزدیک به تموم شدن
        for g in self._goals:
            pct = goal_repo.get_goal_progress_percent(g.id)
            if pct >= 75:
                insights.append(("🎯", "Goal Almost Done!",
                                  f"'{g.name}' is {pct}% complete. Keep pushing!",
                                  "#0a1a2a", BLUE))
                break

        # همه عادت‌های امروز انجام شده
        if self._habits:
            all_done = all(habit_repo.is_habit_done_today(h.id) for h in self._habits)
            if all_done:
                insights.append(("⭐", "Perfect Day!",
                                  "You completed all your habits today. Outstanding!",
                                  "#1a2a1a", GREEN))

        # Focus time بالا
        if self._focus_today >= 3600:
            h = self._focus_today // 3600
            insights.append(("⚡", "Deep Focus Session",
                              f"You've logged {h}h of focus time today. Great work!",
                              "#1a1535", ACCENT2))

        if not insights:
            return None

        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        title = QLabel("Key Insights")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        for i in range(0, len(insights), 2):
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(14)

            for icon, name, desc, bg, col in insights[i:i+2]:
                card = make_card(color=bg)
                cl = QHBoxLayout(card)
                cl.setContentsMargins(16, 14, 16, 14)
                cl.setSpacing(12)
                icon_box = QLabel(icon)
                icon_box.setFixedSize(36, 36)
                icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
                icon_box.setStyleSheet("font-size: 18px; background: rgba(255,255,255,0.08); border-radius: 10px;")
                info = QVBoxLayout()
                info.setSpacing(3)
                n = QLabel(name)
                n.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {col}; background: transparent;")
                d = QLabel(desc)
                d.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
                d.setWordWrap(True)
                info.addWidget(n)
                info.addWidget(d)
                cl.addWidget(icon_box)
                cl.addLayout(info, 1)
                rl.addWidget(card)

            if len(insights[i:i+2]) == 1:
                rl.addStretch()

            lay.addWidget(row)

        return section

    # ─ نمودارهای خطی ─────────────────────────────────────────────────────────
    def _trend_charts(self):
        # داده هفته جاری و ۶ هفته گذشته برای habit score
        today = date.today()
        habit_trend  = []
        focus_trend  = []
        trend_labels = []

        for week_offset in range(6, -1, -1):
            week_start = start_of_week(today) - timedelta(weeks=week_offset)
            week_end   = min(end_of_week(week_start), today) if week_offset == 0 else end_of_week(week_start)

            # habit score این هفته
            if self._habits:
                week_done = []
                for h in self._habits:
                    logs_this_week = habit_repo.count_logs_in_range(h.id,week_start.isoformat(),week_end.isoformat()
)
                    week_done.append(min(logs_this_week / h.frequency_count, 1) * 100)
                habit_trend.append(round(sum(week_done) / len(week_done)))
            else:
                habit_trend.append(0)

            # focus hours این هفته
            focus_h = analytics_repo.get_focus_duration_in_range(week_start.isoformat(),week_end.isoformat())
            focus_trend.append(round(focus_h, 1))

            trend_labels.append(f"W{7 - week_offset}")

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Habit Score Trend
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        t1 = QLabel("Habit Score Trend")
        t1.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(t1)
        ll.addWidget(LineChartDot(habit_trend, trend_labels, ACCENT2, False))

        # Focus Hours Trend
        right = make_card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(20, 18, 20, 18)
        rl.setSpacing(12)
        t2 = QLabel("Weekly Focus Hours")
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl.addWidget(t2)
        rl.addWidget(LineChartDot(focus_trend, trend_labels, GREEN, True))

        lay.addWidget(left, 1)
        lay.addWidget(right, 1)
        return row

    # ─ Radar + Compare ───────────────────────────────────────────────────────
    def _radar_compare_row(self):
        # محاسبه امتیاز هر بخش (0-100)
        habits     = self._habits
        goals      = self._goals
        tasks      = self._tasks

        habit_score = round(sum(1 for h in habits if habit_repo.is_habit_done_today(h.id)) / len(habits) * 100) if habits else 0
        goal_score  = round(sum(goal_repo.get_goal_progress_percent(g.id) for g in goals) / len(goals)) if goals else 0
        task_score  = round(sum(1 for t in tasks if t.done) / len(tasks) * 100) if tasks else 0
        focus_score = min(round(self._focus_today / 3600 / 8 * 100), 100)  # هدف ۸ ساعت

        max_streak  = max((habit_repo.get_current_streak(h.id) for h in habits), default=0)
        streak_score = min(max_streak * 3, 100)  # ۳۳ روز = 100%

        radar_values = [habit_score, goal_score, task_score, focus_score, streak_score]

        # مقایسه این هفته با هفته قبل (focus hours)
        today      = date.today()
        this_start = today - timedelta(days=today.weekday())
        last_start = this_start - timedelta(weeks=1)

        this_week_hours = []
        last_week_hours = []
        week_labels     = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i in range(7):
            d_this = this_start + timedelta(days=i)
            d_last = last_start + timedelta(days=i)
            this_week_hours.append(round(analytics_repo.get_focus_duration_in_range(d_this.isoformat(),d_this.isoformat()),1))

            last_week_hours.append(round(analytics_repo.get_focus_duration_in_range(d_last.isoformat(),d_last.isoformat()),1))

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Performance Radar
        radar_card = make_card()
        rl2 = QVBoxLayout(radar_card)
        rl2.setContentsMargins(20, 18, 20, 18)
        rl2.setSpacing(12)
        tr = QLabel("Performance Radar")
        tr.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl2.addWidget(tr)
        rl2.addWidget(RadarChart(
            labels=["Habits", "Goals", "Tasks", "Focus", "Streak"],
            values=radar_values
        ))

        # Weekly Comparison
        compare_card = make_card()
        cl2 = QVBoxLayout(compare_card)
        cl2.setContentsMargins(20, 18, 20, 18)
        cl2.setSpacing(12)
        tc = QLabel("Focus Hours: This Week vs Last")
        tc.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        cl2.addWidget(tc)
        cl2.addWidget(CompareBarChart(week_labels, this_week_hours, last_week_hours))

        lay.addWidget(radar_card, 1)
        lay.addWidget(compare_card, 2)
        return row

    # ─ Performance Banner ─────────────────────────────────────────────────────
    def _performance_banner(self):
        habits     = self._habits
        goals      = self._goals
        tasks      = self._tasks

        habit_pct  = round(sum(1 for h in habits if habit_repo.is_habit_done_today(h.id)) / len(habits) * 100) if habits else 0
        avg_goal   = round(sum(goal_repo.get_goal_progress_percent(g.id) for g in goals) / len(goals)) if goals else 0
        max_streak = max((habit_repo.get_current_streak(h.id) for h in habits), default=0)

        # پیام بر اساس عملکرد
        if habit_pct == 100:
            msg = "Outstanding Performance! 🌟"
            sub = "You completed all your habits today. You're in the top 5%!"
        elif habit_pct >= 75:
            msg = "Great Work Today! 💪"
            sub = f"You've completed {habit_pct}% of your habits. Keep it up!"
        elif habit_pct >= 50:
            msg = "Good Progress! 📈"
            sub = "You're halfway there. Push a little more today!"
        elif habits:
            msg = "Let's Get Moving! 🚀"
            sub = "Start checking off your habits to see your score climb!"
        else:
            msg = "Welcome to Analytics! 📊"
            sub = "Add habits, goals and tasks to see your performance here."

        card = make_card(color="#1a1535")
        card.setMinimumHeight(160)
        lay = QVBoxLayout(card)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        icon = QLabel("🏅")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 28px; background: rgba(255,255,255,0.08); border-radius: 24px; padding: 10px;")
        icon.setFixedSize(52, 52)

        title = QLabel(msg)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")

        sub_lbl = QLabel(sub)
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        sub_lbl.setWordWrap(True)

        # آمار پایین — فقط اگه داده داشته باشن
        stats_row = QHBoxLayout()
        stats_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stats_row.setSpacing(0)

        stats = []
        if habits:
            stats.append((f"{habit_pct}%", "Habits", ACCENT2))
        if goals:
            stats.append((f"{avg_goal}%", "Goals", BLUE))
        if max_streak > 0:
            stats.append((str(max_streak), "Day Streak", GREEN))

        for j, (val, lbl, col) in enumerate(stats):
            item = QVBoxLayout()
            item.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            v = QLabel(val)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {col}; background: transparent;")
            l = QLabel(lbl)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            item.addWidget(v)
            item.addWidget(l)
            stats_row.addLayout(item)

            if j < len(stats) - 1:
                sep = QFrame()
                sep.setFixedWidth(1)
                sep.setFixedHeight(40)
                sep.setStyleSheet(f"background: rgba(255,255,255,0.12);")
                stats_row.addSpacing(30)
                stats_row.addWidget(sep)
                stats_row.addSpacing(30)

        lay.addWidget(icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addWidget(title)
        lay.addWidget(sub_lbl)
        if stats:
            lay.addLayout(stats_row)

        return card

    # ─ توابع کمکی ────────────────────────────────────────────────────────────
