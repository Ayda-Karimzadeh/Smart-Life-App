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

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def _banner(self):
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
        for icon, txt, col in [("🔥", "24 day streak", ORANGE), ("🏆", "Level 12 Achiever", ACCENT2)]:
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
            ("📈", "92%", "Daily Progress", "Great momentum today!", GREEN, "↑ 8%"),
            ("✅", "3/4", "Habits Completed", "Almost there!", GREEN, ""),
            ("🎯", "3", "Active Goals", "In progress", BLUE, ""),
            ("⏱", "4.5h", "Focus Time Today", "+30 min vs yesterday", ORANGE, "↑ 12%"),
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
        for val, lbl, col in [(92, "Daily Score", ACCENT2), (75, "Weekly Avg", BLUE)]:
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

        chart = LineChart(color=ACCENT2)
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

        tasks = [
            ("Morning meditation", "6:00 AM", True),
            ("Review project goals", "9:00 AM", True),
            ("Workout session", "5:00 PM", False),
            ("Read for 30 minutes", "8:00 PM", False),
        ]

        for name, time, done in tasks:
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
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet(f"""
                font-size: 13px;
                color: {TEXT_MUTED};
                background: transparent;
                {'text-decoration: line-through;' if done else f'color: {TEXT_PRIMARY};'}
            """)
            time_lbl = QLabel(time)
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

        goals = [
            ("Learn Web Development", "Learning", 68, ACCENT2),
            ("Run 100km this month", "Fitness", 72, BLUE),
            ("Read 12 books this year", "Personal", 42, ACCENT),
        ]

        for name, cat, pct, col in goals:
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

        streaks = [
            ("Morning Routine", 24, True, ORANGE),
            ("Exercise", 18, True, ORANGE),
            ("Reading", 21, False, TEXT_MUTED),
            ("Meditation", 30, True, ORANGE),
        ]

        for name, days, done, col in streaks:
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