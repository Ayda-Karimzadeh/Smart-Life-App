import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QScrollArea,
    QProgressBar, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush
import math

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

        title = QLabel("Good evening, Alex! ✨")
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