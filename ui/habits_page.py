from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)


# ─── ویجت: نوار هفتگی (7 مربع رنگی) ─────────────────────────────────────────
class WeekBar(QWidget):
    def __init__(self, done=7, total=7, color=GREEN, parent=None):
        super().__init__(parent)
        self.done = done
        self.total = total
        self.color = color
        self.setFixedHeight(10)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        gap = 6
        count = self.total
        block_w = (w - gap * (count - 1)) / count

        for i in range(count):
            x = i * (block_w + gap)
            color = QColor(self.color) if i < self.done else QColor(BG_CARD2)
            p.setBrush(color)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(int(x), 0, int(block_w), 10, 5, 5)


# ─── کارت عادت ───────────────────────────────────────────────────────────────
class HabitCard(QWidget):
    def __init__(self, icon, name, category, freq, done_week, total_week,
                 current_streak, best_streak, completed_today, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        card = make_card(color="#1a2a1a" if completed_today else BG_CARD)
        card.setMinimumHeight(160)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        # ─ ردیف بالا: آیکون + نام + چک ─
        top = QHBoxLayout()

        icon_box = QLabel(icon)
        icon_box.setFixedSize(44, 44)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet(f"""
            font-size: 22px;
            background: rgba(255,255,255,0.07);
            border-radius: 12px;
        """)

        info = QVBoxLayout()
        info.setSpacing(4)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")

        tags = QHBoxLayout()
        tags.setSpacing(6)
        for tag in [category, freq]:
            t = QLabel(tag)
            t.setStyleSheet(f"""
                font-size: 11px;
                color: {GREEN};
                background: rgba(62,207,142,0.12);
                border-radius: 6px;
                padding: 2px 8px;
            """)
            tags.addWidget(t)
        tags.addStretch()

        info.addWidget(name_lbl)
        info.addLayout(tags)

        check = QLabel("✅" if completed_today else "⭕")
        check.setStyleSheet(f"font-size: 24px; background: transparent;")
        check.setFixedSize(36, 36)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top.addWidget(icon_box)
        top.addSpacing(10)
        top.addLayout(info, 1)
        top.addWidget(check)
        lay.addLayout(top)

        # ─ نوار هفتگی ─
        week_row = QHBoxLayout()
        week_lbl = QLabel("This Week")
        week_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        days_lbl = QLabel(f"{done_week}/{total_week} days")
        days_lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        week_row.addWidget(week_lbl)
        week_row.addStretch()
        week_row.addWidget(days_lbl)
        lay.addLayout(week_row)

        bar = WeekBar(done_week, total_week, GREEN)
        lay.addWidget(bar)

        # ─ Streak ─
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: rgba(255,255,255,0.06);")
        lay.addWidget(sep)

        streak_row = QHBoxLayout()
        cur = QVBoxLayout()
        cur_lbl = QLabel("Current Streak")
        cur_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        cur_val = QLabel(f"🔥 {current_streak} days")
        cur_val.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {ORANGE}; background: transparent;")
        cur.addWidget(cur_lbl)
        cur.addWidget(cur_val)

        best = QVBoxLayout()
        best.setAlignment(Qt.AlignmentFlag.AlignRight)
        best_lbl = QLabel("Best Streak")
        best_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        best_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        best_val = QLabel(f"{best_streak} days")
        best_val.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        best_val.setAlignment(Qt.AlignmentFlag.AlignRight)
        best.addWidget(best_lbl)
        best.addWidget(best_val)

        streak_row.addLayout(cur)
        streak_row.addStretch()
        streak_row.addLayout(best)
        lay.addLayout(streak_row)

        # کارت رو داخل خودمون می‌ذاریم
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)


# ─── صفحه: Habits ────────────────────────────────────────────────────────────
class HabitsPage(QWidget):
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
        layout.addWidget(self._filter_row())
        layout.addWidget(self._habits_grid())
        layout.addStretch()

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    # ─ ۴ کارت آمار بالا ─────────────────────────────────────────────────────
    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("✅", "63%", "Today's Completion", "5 of 8 habits", ACCENT, True),
            ("🔥", "30", "Longest Streak", "Morning Meditation", ORANGE, False),
            ("📈", "85%", "Weekly Average", "Up 12% from last week", GREEN, False),
            ("🏆", "8", "Active Habits", "Building consistency", ORANGE, False),
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
            val_lbl.setStyleSheet(
                f"font-size: 30px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
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

    # ─ فیلتر دسته‌بندی ───────────────────────────────────────────────────────
    def _filter_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        categories = ["All", "Mindfulness", "Fitness", "Health", "Personal Growth", "Skills", "Digital Wellness"]

        for i, cat in enumerate(categories):
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            active = i == 0
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'%s' % ACCENT if active else 'transparent'};
                    color: {'white' if active else TEXT_MUTED};
                    border: 1px solid {'transparent' if active else 'rgba(255,255,255,0.12)'};
                    border-radius: 16px;
                    padding: 6px 14px;
                    font-size: 12px;
                    font-weight: {'600' if active else '400'};
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,0.07);
                    color: {TEXT_PRIMARY};
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lay.addWidget(btn)

        lay.addStretch()
        return row

    # ─ گرید عادت‌ها ──────────────────────────────────────────────────────────
    def _habits_grid(self):
        grid = QWidget()
        grid.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(grid)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        habits = [
            ("🧘", "Morning Meditation", "Mindfulness", "Daily", 7, 7, 30, 45, True),
            ("💪", "Exercise", "Fitness", "Daily", 6, 7, 18, 28, True),
            ("📚", "Reading", "Personal Growth", "Daily", 6, 7, 21, 35, False),
            ("💧", "Drink 8 Glasses", "Health", "Daily", 7, 7, 24, 30, True),
            ("🎸", "Practice Guitar", "Skills", "3x per week", 3, 7, 4, 8, False),
            ("📓", "Journal", "Mindfulness", "Daily", 6, 7, 15, 22, True),
            ("🚫", "No Social Media Before Noon", "Digital Wellness", "Daily", 6, 7, 12, 18, True),
            ("🥗", "Cook Healthy Meal", "Health", "5x per week", 4, 7, 6, 10, False),
        ]

        # دو تا در هر ردیف
        for i in range(0, len(habits), 2):
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(14)

            for h in habits[i:i + 2]:
                icon, name, cat, freq, dw, tw, cs, bs, done = h
                rl.addWidget(HabitCard(icon, name, cat, freq, dw, tw, cs, bs, done))

            if len(habits[i:i + 2]) == 1:
                rl.addStretch()

            lay.addWidget(row)

        add_card = QFrame()
        add_card.setMinimumHeight(80)
        add_card.setStyleSheet(f"""
                QFrame {{
                    background: transparent;
                    border: 2px dashed rgba(255,255,255,0.12);
                    border-radius: 14px;
                }}
            """)
        add_lay = QVBoxLayout(add_card)
        add_btn = QLabel("+ Add New Habit")
        add_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_btn.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        add_lay.addWidget(add_btn)
        lay.addWidget(add_card)

        return grid