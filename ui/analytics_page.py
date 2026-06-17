import math
from re import sub
from turtle import title
from PyQt6.QtWidgets import (
    QFrame, QFrame, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF, QPainterPath, QFont

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)

class LineChartDot(QWidget):
    def __init__(self, data=None, color=ACCENT2, filled=False, parent=None):
        super().__init__(parent)
        self.data = data or [72, 78, 75, 82, 80, 88, 92]
        self.color = color
        self.filled = filled
        self.labels = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
        self.setMinimumHeight(180)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 30
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        mn, mx = 0, 100
        rang = mx - mn

        pts = []
        for i, v in enumerate(self.data):
            x = pad_l + i * chart_w / (len(self.data) - 1)
            y = pad_t + chart_h - (v - mn) / rang * chart_h
            pts.append((x, y))

        # خطوط راهنما
        for i in range(5):
            val = 100 - i * 25
            y = pad_t + i * chart_h // 4
            p.setPen(QPen(QColor(50, 50, 70), 1))
            p.drawLine(pad_l, int(y), w - pad_r, int(y))
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, int(y) - 6, pad_l - 4, 14,
                       Qt.AlignmentFlag.AlignRight, str(val))

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

        # برچسب روزها
        p.setPen(QColor(TEXT_MUTED))
        p.setFont(QFont("Segoe UI", 9))
        for i, lbl in enumerate(self.labels):
            x = pad_l + i * chart_w / (len(self.data) - 1)
            p.drawText(int(x) - 15, h - pad_b + 6, 30, 20,
                       Qt.AlignmentFlag.AlignHCenter, lbl)

# ─── نمودار رادار (عنکبوتی) ──────────────────────────────────────────────────
class RadarChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels = ["Habits", "Goals", "Tasks", "Time Mgmt", "Consistency"]
        self.values = [88, 68, 75, 82, 72]  # 0-100
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

        # خطوط محور
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
            rr = r * v / 100
            pts.append(QPointF(cx + rr * math.cos(angle), cy - rr * math.sin(angle)))

        fill = QColor(ACCENT)
        fill.setAlpha(60)
        p.setBrush(QBrush(fill))
        p.setPen(QPen(QColor(ACCENT2), 2))
        p.drawPolygon(QPolygonF(pts))

        # نقاط
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


# ─── نمودار مقایسه‌ای ─────────────────────────────────────────────────────────
class CompareBarChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        self.last  = [68, 72, 70, 74]
        self.this  = [72, 78, 74, 80]
        self.setMinimumHeight(220)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 40
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        n = len(self.labels)
        group_w = chart_w / n
        bar_w = int(group_w * 0.3)
        gap = 4

        # خطوط راهنما
        for i in range(5):
            val = 100 - i * 25
            y = int(pad_t + i * chart_h / 4)
            p.setPen(QPen(QColor(50, 50, 70), 1))
            p.drawLine(pad_l, y, w - pad_r, y)
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, y - 6, pad_l - 4, 14,
                       Qt.AlignmentFlag.AlignRight, str(val))

        for i, (lv, tv) in enumerate(zip(self.last, self.this)):
            gx = pad_l + i * group_w + group_w / 2

            # Last Month
            bh = int(lv / 100 * chart_h)
            x1 = int(gx - bar_w - gap / 2)
            p.setBrush(QBrush(QColor(100, 100, 130)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(x1, pad_t + chart_h - bh, bar_w, bh, 4, 4)

            # This Month
            bh2 = int(tv / 100 * chart_h)
            x2 = int(gx + gap / 2)
            p.setBrush(QBrush(QColor(ACCENT2)))
            p.drawRoundedRect(x2, pad_t + chart_h - bh2, bar_w, bh2, 4, 4)

            # برچسب
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(int(gx) - 25, h - pad_b + 6, 50, 20,
                       Qt.AlignmentFlag.AlignHCenter, self.labels[i])

        # legend
        p.setFont(QFont("Segoe UI", 10))
        lx = pad_l + 10
        ly = h - 18
        p.setBrush(QBrush(QColor(100, 100, 130)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(lx, ly, 12, 12)
        p.setPen(QColor(TEXT_MUTED))
        p.drawText(lx + 16, ly - 1, 80, 14, Qt.AlignmentFlag.AlignLeft, "Last Month")

        lx2 = lx + 110
        p.setBrush(QBrush(QColor(ACCENT2)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(lx2, ly, 12, 12)
        p.setPen(QColor(ACCENT2))
        p.drawText(lx2 + 16, ly - 1, 80, 14, Qt.AlignmentFlag.AlignLeft, "This Month")

# ─── صفحه: Analytics ─────────────────────────────────────────────────────────
class AnalyticsPage(QWidget):
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

        layout.addWidget(self._stats_row())
        layout.addWidget(self._insights())
        layout.addWidget(self._charts_row())
        layout.addStretch()

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

        layout.addWidget(self._performance_banner())  # ← اضافه کن
        layout.addStretch()
    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("📈", "92",   "Productivity Score", "This week",       ACCENT2, True,  "+18%",     GREEN),
            ("💚", "88%",  "Habit Consistency",  "Monthly average", GREEN,   False, "+12%",     GREEN),
            ("🎯", "56%",  "Goal Completion",    "Average progress",BLUE,    False, "+8%",      GREEN),
            ("📅", "24",   "Current Streak",     "Days active",     ORANGE,  False, "Best yet!",ORANGE),
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
            icon_box.setStyleSheet(f"""
                font-size: 20px;
                background: rgba(255,255,255,0.07);
                border-radius: 10px;
            """)
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
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        title = QLabel("Key Insights")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        insights = [
            ("📈", "Excellent Week!",    "Your productivity score increased by 18% compared to last week", "#1a2a1a", GREEN),
            ("🏆", "30-Day Streak",      "You've maintained your meditation habit for a full month!",       "#2a1a0a", ORANGE),
            ("🎯", "Goal Progress",      "You're 68% towards your web development goal. Keep it up!",       "#0a1a2a", BLUE),
            ("⚡", "Peak Productivity",  "Your most productive hours are between 9 AM - 12 PM",             "#1a1535", ACCENT2),
        ]

        # دو تا در هر ردیف
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
                icon_box.setStyleSheet(f"""
                    font-size: 18px;
                    background: rgba(255,255,255,0.08);
                    border-radius: 10px;
                """)

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

            lay.addWidget(row)

        return section

    # ─ نمودارها ──────────────────────────────────────────────────────────────
    def _charts_row(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        main_lay = QVBoxLayout(container)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(14)

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Productivity Trend
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        t1 = QLabel("Productivity Trend")
        t1.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(t1)
        ll.addWidget(LineChartDot(
            data=[72, 78, 75, 82, 80, 88, 92],
            color=ACCENT2, filled=False
        ))

        # Habit Consistency
        right = make_card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(20, 18, 20, 18)
        rl.setSpacing(12)
        t2 = QLabel("Habit Consistency")
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl.addWidget(t2)
        rl.addWidget(LineChartDot(
            data=[60, 65, 70, 72, 78, 82, 88],
            color=GREEN, filled=True
        ))

        lay.addWidget(left, 1)
        lay.addWidget(right, 1)
        main_lay.addWidget(row)

        row2 = QWidget()
        row2.setStyleSheet("background: transparent;")
        lay2 = QHBoxLayout(row2)
        lay2.setContentsMargins(0, 0, 0, 0)
        lay2.setSpacing(14)

        radar_card = make_card()
        rl2 = QVBoxLayout(radar_card)
        rl2.setContentsMargins(20, 18, 20, 18)
        rl2.setSpacing(12)
        tr = QLabel("Performance Radar")
        tr.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl2.addWidget(tr)
        rl2.addWidget(RadarChart())

        compare_card = make_card()
        cl2 = QVBoxLayout(compare_card)
        cl2.setContentsMargins(20, 18, 20, 18)
        cl2.setSpacing(12)
        tc = QLabel("Weekly Progress Comparison")
        tc.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        cl2.addWidget(tc)
        cl2.addWidget(CompareBarChart())

        lay2.addWidget(radar_card, 1)
        lay2.addWidget(compare_card, 2)
        main_lay.addWidget(row2)

        return container
    
    def _performance_banner(self):
        card = make_card(color="#1a1535")
        card.setMinimumHeight(160)
        lay = QVBoxLayout(card)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)

        icon = QLabel("🏅")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("""
            font-size: 28px;
            background: rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 10px;
        """)
        icon.setFixedSize(52, 52)

        title = QLabel("Outstanding Performance!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")

        sub = QLabel("You're in the top 5% of users this month. Your consistency and dedication are paying off!")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        sub.setWordWrap(True)

        # ─ آمار پایین ─
        stats = QHBoxLayout()
        stats.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stats.setSpacing(0)

        for val, lbl, col in [("92%", "Productivity", ACCENT2), ("88%", "Consistency", BLUE), ("24", "Day Streak", GREEN)]:
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

            stats.addLayout(item)

            # خط جداکننده
            if lbl != "Day Streak":
                sep = QFrame()
                sep.setFixedWidth(1)
                sep.setFixedHeight(40)
                sep.setStyleSheet(f"background: rgba(255,255,255,0.12);")
                stats.addSpacing(30)
                stats.addWidget(sep)
                stats.addSpacing(30)

        lay.addWidget(icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addLayout(stats)
        return card