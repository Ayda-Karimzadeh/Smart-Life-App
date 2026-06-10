from turtle import title

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)


# ─── نمودار میله‌ای ───────────────────────────────────────────────────────────
class BarChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        # (روز, ساعت)
        self.data = data or [
            ("Mon", 3.5), ("Tue", 8.0), ("Wed", 5.0),
            ("Thu", 9.5), ("Fri", 6.5), ("Sat", 4.0), ("Sun", 7.0)
        ]
        self.setMinimumHeight(200)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 30
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        max_val = max(v for _, v in self.data) or 1
        bar_count = len(self.data)
        bar_w = int(chart_w / bar_count * 0.5)
        gap = chart_w / bar_count

        # خطوط راهنما
        for i in range(5):
            y = pad_t + i * chart_h // 4
            p.setPen(QPen(QColor("rgba(255,255,255,20)"), 1))
            p.drawLine(pad_l, y, w - pad_r, y)
            val = max_val - i * max_val / 4
            p.setPen(QColor(TEXT_MUTED))
            from PyQt6.QtGui import QFont
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, y + 5, pad_l - 4, 14, Qt.AlignmentFlag.AlignRight, f"{val:.0f}")

        # میله‌ها
        for i, (day, val) in enumerate(self.data):
            bar_h = int(val / max_val * chart_h)
            x = int(pad_l + i * gap + (gap - bar_w) / 2)
            y = pad_t + chart_h - bar_h

            # میله
            p.setBrush(QBrush(QColor(GREEN)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(x, y, bar_w, bar_h, 4, 4)

            # برچسب روز
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(x - 5, h - pad_b + 6, bar_w + 10, 20,
                       Qt.AlignmentFlag.AlignHCenter, day)


# ─── نمودار دونات ─────────────────────────────────────────────────────────────
class DonutChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        # (نام, مقدار, رنگ)
        self.data = data or [
            ("Study",    22, ACCENT2),
            ("Work",     18, BLUE),
            ("Exercise",  8, GREEN),
            ("Personal", 12, ORANGE),
            ("Other",     7, RED),
        ]
        self.setMinimumSize(200, 200)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height()) - 20
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2

        total = sum(v for _, v, _ in self.data)
        start = 90 * 16
        thickness = 28

        for name, val, color in self.data:
            span = int(val / total * 360 * 16)
            p.setPen(QPen(QColor(color), thickness,
                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.setBrush(Qt.BrushStyle.NoBrush)
            margin = thickness // 2
            p.drawArc(x + margin, y + margin,
                      size - thickness, size - thickness, start, -span)
            start -= span


# ─── صفحه: Time Tracking ─────────────────────────────────────────────────────
class TimerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        self._seconds = 0
        self._running = False

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        layout.addWidget(self._stats_row())
        layout.addWidget(self._timer_banner())
        layout.addWidget(self._charts_row())
        layout.addWidget(self._recent_sessions())
        layout.addStretch()

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

        # تایمر واقعی
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    # ─ آمار ──────────────────────────────────────────────────────────────────
    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("⏱",  "4.5h", "Focused Today",  "+30 min vs yesterday",  ACCENT2, True),
            ("📈", "67h",  "This Week",       "Across all categories", BLUE,    False),
            ("📖", "22h",  "Study Time",      "Most time spent",       ACCENT,  False),
            ("📅", "9.6h", "Daily Average",   "This week",             GREEN,   False),
        ]

        for icon, val, title, sub, col, highlight in items:
            card = make_card(color="#1a1535" if highlight else BG_CARD)
            card.setMinimumHeight(120)
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
            top.addWidget(icon_box)
            top.addStretch()

            val_lbl = QLabel(val)
            val_lbl.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
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

    # ─ بنر تایمر ─────────────────────────────────────────────────────────────
    def _timer_banner(self):
        card = make_card(color="#1a1535")
        card.setMinimumHeight(160)
        lay = QVBoxLayout(card)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        title = QLabel("Ready to Focus?")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")

        sub = QLabel("Start a new focus session and track your productivity")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")

        # نمایش زمان
        self.time_lbl = QLabel("00:00:00")
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_lbl.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {ACCENT2}; background: transparent;")

        # دکمه Start/Stop
        self.start_btn = QPushButton("▶  Start Timer")
        self.start_btn.setFixedSize(160, 46)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        self.start_btn.clicked.connect(self._toggle_timer)

        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addWidget(self.time_lbl)
        lay.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        return card

    # ─ نمودارها ──────────────────────────────────────────────────────────────
    def _charts_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Weekly Activity
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        t1 = QLabel("Weekly Activity")
        t1.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(t1)
        ll.addWidget(BarChart())

        legend = QHBoxLayout()
        legend.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        legend.setSpacing(16)
        for name, col in [("study", ACCENT2), ("work", BLUE), ("fitness", ORANGE), ("personal", GREEN)]:
            row_l = QHBoxLayout()
            dot = QLabel("■")
            dot.setStyleSheet(f"color: {col}; background: transparent; font-size: 11px;")
            lbl = QLabel(name)
            lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            row_l.addWidget(dot)
            row_l.addWidget(lbl)
            legend.addLayout(row_l)
        ll.addLayout(legend)

        # Time Distribution
        right = make_card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(20, 18, 20, 18)
        rl.setSpacing(12)
        t2 = QLabel("Time Distribution")
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl.addWidget(t2)

        donut = DonutChart()
        donut.setMinimumHeight(200)
        rl.addWidget(donut)

        # راهنما
        legend_data = [
            ("Study",    22, ACCENT2),
            ("Work",     18, BLUE),
            ("Exercise",  8, GREEN),
            ("Personal", 12, ORANGE),
            ("Other",     7, RED),
        ]
        for name, val, col in legend_data:
            row2 = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {col}; background: transparent; font-size: 12px;")
            dot.setFixedWidth(16)
            n = QLabel(name)
            n.setStyleSheet(f"font-size: 12px; color: {TEXT_PRIMARY}; background: transparent;")
            v = QLabel(f"{val}h")
            v.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            row2.addWidget(dot)
            row2.addWidget(n, 1)
            row2.addWidget(v)
            rl.addLayout(row2)

        lay.addWidget(left, 2)
        lay.addWidget(right, 1)
        return row

    # ─ منطق تایمر ────────────────────────────────────────────────────────────
    def _toggle_timer(self):
        if self._running:
            self._timer.stop()
            self._running = False
            self.start_btn.setText("▶  Start Timer")
            self.start_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ACCENT};
                    color: white; border: none;
                    border-radius: 14px;
                    font-size: 14px; font-weight: 600;
                }}
                QPushButton:hover {{ background: {ACCENT2}; }}
            """)
        else:
            self._timer.start(1000)
            self._running = True
            self.start_btn.setText("⏹  Stop Timer")
            self.start_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {RED};
                    color: white; border: none;
                    border-radius: 14px;
                    font-size: 14px; font-weight: 600;
                }}
                QPushButton:hover {{ background: #c04040; }}
            """)

    def _tick(self):
        self._seconds += 1
        h = self._seconds // 3600
        m = (self._seconds % 3600) // 60
        s = self._seconds % 60
        self.time_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")


    def _recent_sessions(self):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        title = QLabel("Recent Sessions")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        sessions = [
            ("📖", "React Development", "Study", "Today, 2:00 PM",  "2h 30m", ACCENT2),
            ("💼", "Project Meeting",   "Work",  "Today, 10:00 AM", "1h 15m", BLUE),
            ("🏃", "Morning Run",       "Fitness","Today, 7:00 AM", "45m",    GREEN),
            ("📚", "Spanish Practice",  "Study", "Yesterday, 8PM",  "1h 00m", ACCENT2),
        ]

        for icon, name, cat, time, duration, col in sessions:
            card = make_card(color=BG_CARD2)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(16, 12, 16, 12)
            cl.setSpacing(14)

            icon_box = QLabel(icon)
            icon_box.setFixedSize(40, 40)
            icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_box.setStyleSheet(f"""
                font-size: 20px;
                background: rgba(255,255,255,0.07);
                border-radius: 10px;
            """)

            info = QVBoxLayout()
            info.setSpacing(3)
            n = QLabel(name)
            n.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
            t = QLabel(f"{cat}  •  {time}")
            t.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            info.addWidget(n)
            info.addWidget(t)

            dur_col = QVBoxLayout()
            dur_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            d = QLabel(duration)
            d.setAlignment(Qt.AlignmentFlag.AlignRight)
            d.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
            dl = QLabel("Duration")
            dl.setAlignment(Qt.AlignmentFlag.AlignRight)
            dl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            dur_col.addWidget(d)
            dur_col.addWidget(dl)

            cl.addWidget(icon_box)
            cl.addLayout(info, 1)
            cl.addLayout(dur_col)
            lay.addWidget(card)

        return section