from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPolygonF, QPainterPath

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED, ACCENT,
    ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)
from database import db_manager as db

class CircleChart(QWidget):
    def __init__(self, value=92, label="", color=ACCENT2, parent=None):
        super().__init__(parent)
        self.value = value
        self.label = label
        self.color = color
        self.setFixedSize(130, 130)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height()) - 16
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2

        # پس‌زمینه
        p.setPen(QPen(QColor(BG_CARD2), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(x, y, size, size, 0, 360 * 16)

        # پیشرفت
        span = int(self.value / 100 * 360 * 16)
        p.setPen(QPen(QColor(self.color), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(x, y, size, size, 90 * 16, -span)

        # متن درصد
        p.setPen(QColor(TEXT_PRIMARY))
        p.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.value}%")


# ─── ویجت: نمودار خطی ساده ───────────────────────────────────────────────────
class LineChart(QWidget):
    def __init__(self, data=None, color=ACCENT2, parent=None):
        super().__init__(parent)
        self.data = data or [72, 85, 78, 91, 88, 95, 92, 89, 97, 93, 96, 98, 95, 99]
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
            x = pad + i * (w - 2 * pad) / (len(self.data) - 1)
            y = h - pad - (v - mn) / rang * (h - 2 * pad)
            pts.append((x, y))

        # سطح زیر نمودار
        fill_color = QColor(self.color)
        fill_color.setAlpha(40)
        p.setBrush(QBrush(fill_color))
        p.setPen(Qt.PenStyle.NoPen)
        poly_pts = [(pad, h - pad)] + pts + [(w - pad, h - pad)]
        from PyQt6.QtGui import QPolygonF
        from PyQt6.QtCore import QPointF
        poly = QPolygonF([QPointF(x, y) for x, y in poly_pts])
        p.drawPolygon(poly)

        # خط
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(self.color), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        from PyQt6.QtGui import QPainterPath
        path = QPainterPath()
        path.moveTo(pts[0][0], pts[0][1])
        for x, y in pts[1:]:
            path.lineTo(x, y)
        p.drawPath(path)


# ─── صفحه: داشبورد ───────────────────────────────────────────────────────────
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        
        # ─ داده‌های پایه از دیتابیس ─────────────────────────────────────
        self.habits = db.get_all_habits()
        self.goals = db.get_all_goals()
        self.tasks = db.get_all_tasks(done=False)  # فقط تسک‌های انجام نشده
        
        # محاسبه درصد‌ها
        self.habits_completed_today = sum(1 for h in self.habits if db.is_habit_done_today(h.id))
        self.daily_progress = int((self.habits_completed_today / len(self.habits) * 100)) if self.habits else 0
        self.weekly_avg = self._calculate_weekly_avg()
        
        # زمان فوکوس امروز (به ساعت)
        total_seconds = db.get_total_time_today()
        self.focus_time_today = f"{total_seconds / 3600:.1f}h" if total_seconds > 0 else "0h"
        
        # داده‌های نمودار
        self.weekly_activity_data = self._get_weekly_activity_data()
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        # بنر خوش‌آمدگویی
        layout.addWidget(self._banner())

        # کارت‌های آمار
        layout.addWidget(self._stats_row())

        # پایین: نمودارها
        layout.addWidget(self._charts_row())

        layout.addWidget(self._tasks_goals_row())  # ← این
        layout.addWidget(self._habit_streaks())  # ← و این

        layout.addStretch()
        scroll.setWidget(content)

        self.scroll_content = content  # احفظ المرجع
        self.scroll = scroll
        self.main_layout = layout

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)
    
    def showEvent(self, event):
        """هر بار که صفحه نمایش داده می‌شود، داده‌ها را تازه کن"""
        super().showEvent(event)
        self._refresh_data()
    
    def _refresh_data(self):
        """تازه کردن تمام داده‌ها از دیتابیس و به‌روزرسانی واجهه"""
        self.habits = db.get_all_habits()
        self.goals = db.get_all_goals()
        self.tasks = db.get_all_tasks(done=False)
        
        self.habits_completed_today = sum(1 for h in self.habits if db.is_habit_done_today(h.id))
        self.daily_progress = int((self.habits_completed_today / len(self.habits) * 100)) if self.habits else 0
        self.weekly_avg = self._calculate_weekly_avg()
        
        total_seconds = db.get_total_time_today()
        self.focus_time_today = f"{total_seconds / 3600:.1f}h" if total_seconds > 0 else "0h"
        
        self.weekly_activity_data = self._get_weekly_activity_data()
        
        # تعديل محتوی layout (بدون نیاز به ساخت مجدد)
        # این روش سریع‌تر است
    
    def _calculate_weekly_avg(self):
        """میانگین درصد انجام این هفته"""
        if not self.habits:
            return 0
        
        total = sum(db.get_week_progress(h.id) for h in self.habits)
        avg = (total / len(self.habits) / 7) * 100 if self.habits else 0
        return int(min(avg, 100))
    
    def _get_weekly_activity_data(self):
        """داده‌های فعالیت هفتگی برای نمودار (بر اساس جلسات فعلی زمانی)"""
        weekly_activity = db.get_weekly_activity()
        
        # تبدیل ساعات به درجه 0-100 (حداکثر 8 ساعت = 100)
        max_hours = 8
        data = []
        for day_name, hours in weekly_activity:
            score = min(int((hours / max_hours) * 100), 100)
            data.append(score)
        
        return data if data else [0] * 7

    def _banner(self):
        # پیدا کردن بیشترین streak
        max_streak = max([db.get_current_streak(h.id) for h in self.habits], default=0)
        
        card = make_card(color="#1a1530")
        card.setMinimumHeight(150)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 22, 28, 22)
        lay.setSpacing(10)

        title = QLabel("Good evening!✨")
        title.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        sub = QLabel("You're doing amazing! Keep pushing forward on your journey to greatness.")
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")

        badges = QHBoxLayout()
        streak_txt = f"{max_streak} day streak" if max_streak > 0 else "Start your streak!"
        for icon, txt, col in [("🔥", streak_txt, ORANGE), ("🏆", "Level 12 Achiever", ACCENT2)]:
            btn = QPushButton(f"  {icon}  {txt}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255,255,255,0.07);
                    color: {col};
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 18px;
                    padding: 6px 16px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            badges.addWidget(btn)
        badges.addStretch()

        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addLayout(badges)
        return card

    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("📈", f"{self.daily_progress}%", "Daily Progress", "Great momentum today!", GREEN, "↑ 8%"),
            ("✅", f"{self.habits_completed_today}/{len(self.habits)}", "Habits Completed", "Almost there!", GREEN, ""),
            ("🎯", str(len(self.goals)), "Active Goals", "In progress", BLUE, ""),
            ("⏱", self.focus_time_today, "Focus Time Today", "Time tracking", ORANGE, ""),
        ]

        for icon, val, title, sub, col, badge in items:
            card = make_card()
            card.setMinimumHeight(130)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(4)

            top = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet(f"""
                font-size: 20px;
                background: rgba(255,255,255,0.07);
                border-radius: 10px;
                padding: 6px;
            """)
            icon_lbl.setFixedSize(40, 40)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            top.addWidget(icon_lbl)
            top.addStretch()
            if badge:
                b = QLabel(badge)
                b.setStyleSheet(f"color: {GREEN}; font-size: 12px; background: transparent; font-weight: 600;")
                top.addWidget(b)

            val_lbl = QLabel(val)
            val_lbl.setStyleSheet(
                f"font-size: 28px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
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

    def _charts_row(self):
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
        title = QLabel("Today's Overview")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(title)

        circles = QHBoxLayout()
        for val, lbl, col in [(self.daily_progress, "Daily Score", ACCENT2), (self.weekly_avg, "Weekly Avg", BLUE)]:
            vbox = QVBoxLayout()
            vbox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            c = CircleChart(val, lbl, col)
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
        ps = QLabel("Productivity Score")
        ps.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        rtop.addWidget(t2)
        rtop.addStretch()
        rtop.addWidget(ps)

        chart = LineChart(data=self.weekly_activity_data, color=ACCENT2)
        chart.setMinimumHeight(160)

        rl.addLayout(rtop)
        rl.addWidget(chart)

        lay.addWidget(left, 1)
        lay.addWidget(right, 2)
        return row

    def _tasks_goals_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # ── Today's Tasks ──────────────────────────────────────
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)

        # هدر
        header = QHBoxLayout()
        t = QLabel("Today's Tasks")
        t.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        add_btn = QPushButton("+ Add Task")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(t)
        header.addStretch()
        header.addWidget(add_btn)
        ll.addLayout(header)

        for task in self.tasks[:4]:  # نمایش تا ۴ تسک
            done = task.done
            card = make_card(color="#1a2a1a" if done else BG_CARD2)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(14, 10, 14, 10)
            cl.setSpacing(12)

            # دایره چک
            check = QLabel("●")
            check.setStyleSheet(f"""
                font-size: 18px;
                color: {GREEN if done else TEXT_MUTED};
                background: transparent;
            """)
            check.setFixedWidth(22)

            info = QVBoxLayout()
            info.setSpacing(2)
            name_lbl = QLabel(task.name)
            name_lbl.setStyleSheet(f"""
                font-size: 13px;
                color: {TEXT_MUTED};
                background: transparent;
                {'text-decoration: line-through;' if done else f'color: {TEXT_PRIMARY};'}
            """)
            time_lbl = QLabel(task.due_time or "No time")
            time_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            info.addWidget(name_lbl)
            info.addWidget(time_lbl)

            cl.addWidget(check)
            cl.addLayout(info, 1)
            ll.addWidget(card)

        # ── Active Goals ───────────────────────────────────────
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

        for goal in self.goals[:3]:  # نمایش تا ۳ هدف
            pct = db.get_goal_progress(goal.id)
            cat = goal.category
            name = goal.name
            
            # انتخاب رنگ بر اساس category
            col_map = {"Learning": ACCENT2, "Fitness": BLUE, "Personal": ACCENT, "Health": GREEN}
            col = col_map.get(cat, ACCENT2)
            gc = make_card(color=BG_CARD2)
            gl = QVBoxLayout(gc)
            gl.setContentsMargins(14, 12, 14, 12)
            gl.setSpacing(6)

            top = QHBoxLayout()
            n = QLabel(name)
            n.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
            p = QLabel(f"{pct}%")
            p.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {col}; background: transparent;")
            top.addWidget(n)
            top.addStretch()
            top.addWidget(p)

            cat_lbl = QLabel(cat)
            cat_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(pct)
            bar.setTextVisible(False)
            bar.setFixedHeight(6)
            bar.setStyleSheet(f"""
                QProgressBar {{ background: {BG_CARD}; border-radius: 3px; }}
                QProgressBar::chunk {{ background: {col}; border-radius: 3px; }}
            """)

            gl.addLayout(top)
            gl.addWidget(cat_lbl)
            gl.addWidget(bar)
            rl.addWidget(gc)

        rl.addStretch()

        lay.addWidget(left, 1)
        lay.addWidget(right, 1)
        return row

    def _habit_streaks(self):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        title = QLabel("Habit Streaks")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(14)

        for habit in self.habits[:4]:  # نمایش تا ۴ عادت
            days = db.get_current_streak(habit.id)
            done = db.is_habit_done_today(habit.id)
            name = habit.name
            col = ORANGE if done else TEXT_MUTED
            card = make_card(color="#2a1a0a" if done else BG_CARD2)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(6)

            top = QHBoxLayout()
            fire = QLabel("🔥" if done else "🩶")
            fire.setStyleSheet("font-size: 18px; background: transparent;")
            days_lbl = QLabel(f"{days} days")
            days_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {col}; background: transparent;")
            top.addWidget(fire)
            top.addStretch()
            top.addWidget(days_lbl)

            n = QLabel(name)
            n.setStyleSheet(f"font-size: 13px; font-weight: 500; color: {TEXT_PRIMARY}; background: transparent;")
            status = QLabel("Completed today" if done else "Not completed yet")
            status.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

            cl.addLayout(top)
            cl.addWidget(n)
            cl.addWidget(status)
            rl.addWidget(card)

        lay.addWidget(row)
        return section