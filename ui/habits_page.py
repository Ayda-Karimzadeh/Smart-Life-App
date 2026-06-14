from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)
from database import db_manager as db


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


class HabitCard(QWidget):
    """
    کارت یه عادت. روی کلیک دکمه چک، وضعیت امروز toggle می‌شه
    و on_toggle (تابعی که از بیرون پاس داده می‌شه) صدا زده می‌شه.
    """
    def __init__(self, habit, on_toggle, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.on_toggle = on_toggle
        self.setStyleSheet("background: transparent;")

        # داده‌های زنده از دیتابیس
        completed_today = db.is_habit_done_today(habit.id)
        done_week = db.get_week_progress(habit.id)
        total_week = habit.frequency_count
        current_streak = db.get_current_streak(habit.id)
        best_streak = db.get_best_streak(habit.id)

        # فریکانس برای نمایش
        if habit.frequency_type == "daily":
            freq_text = "Daily"
        else:
            freq_text = f"{habit.frequency_count}x per week"

        card = make_card(color="#1a2a1a" if completed_today else BG_CARD)
        card.setMinimumHeight(160)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        top = QHBoxLayout()
        icon_box = QLabel(habit.icon)
        icon_box.setFixedSize(44, 44)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet("font-size: 22px; background: rgba(255,255,255,0.07); border-radius: 12px;")

        info = QVBoxLayout()
        info.setSpacing(4)
        name_lbl = QLabel(habit.name)
        name_lbl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        tags = QHBoxLayout()
        tags.setSpacing(6)
        for tag in [habit.category, freq_text]:
            t = QLabel(tag)
            t.setStyleSheet(f"font-size: 11px; color: {GREEN}; background: rgba(62,207,142,0.12); border-radius: 6px; padding: 2px 8px;")
            tags.addWidget(t)
        tags.addStretch()
        info.addWidget(name_lbl)
        info.addLayout(tags)

        # دکمه چک — قابل کلیک
        self.check_btn = QPushButton("✅" if completed_today else "⭕")
        self.check_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.08);
                border-radius: 8px;
            }
        """)
        self.check_btn.setFixedSize(36, 36)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.clicked.connect(self._handle_toggle)

        top.addWidget(icon_box)
        top.addSpacing(10)
        top.addLayout(info, 1)
        top.addWidget(self.check_btn)
        lay.addLayout(top)

        week_row = QHBoxLayout()
        week_lbl = QLabel("This Week")
        week_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        days_lbl = QLabel(f"{done_week}/{total_week} days")
        days_lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        week_row.addWidget(week_lbl)
        week_row.addStretch()
        week_row.addWidget(days_lbl)
        lay.addLayout(week_row)
        lay.addWidget(WeekBar(done_week, total_week, GREEN))

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

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

    def _handle_toggle(self):
        db.toggle_habit_today(self.habit.id)
        self.on_toggle()   # به صفحه می‌گه که خودش رو دوباره بسازه


class HabitsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.selected_category = "All"
        self.refresh()

    # ─ بازسازی کامل صفحه با داده‌های تازه از دیتابیس ───────────────────────────
    def refresh(self):
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        layout.addWidget(self._stats_row())
        layout.addWidget(self._filter_row())
        layout.addWidget(self._habits_grid())
        layout.addStretch()

        self.scroll.setWidget(content)

    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        habits = db.get_all_habits()
        total = len(habits)

        # امروز چندتا انجام شده
        done_today = sum(1 for h in habits if db.is_habit_done_today(h.id))
        today_pct = round(done_today / total * 100) if total else 0

        # طولانی‌ترین استریک
        if habits:
            best_per_habit = [(h, db.get_best_streak(h.id)) for h in habits]
            longest_habit, longest_streak = max(best_per_habit, key=lambda x: x[1])
            longest_name = longest_habit.name if longest_streak > 0 else "—"
        else:
            longest_streak, longest_name = 0, "—"

        # میانگین هفتگی (٪)
        if habits:
            week_pcts = []
            for h in habits:
                done_week = db.get_week_progress(h.id)
                week_pcts.append(min(done_week / h.frequency_count, 1) * 100)
            weekly_avg = round(sum(week_pcts) / len(week_pcts))
        else:
            weekly_avg = 0

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("✅", f"{today_pct}%", "Today's Completion", f"{done_today} of {total} habits", ACCENT, True),
            ("🔥", str(longest_streak), "Longest Streak", longest_name, ORANGE, False),
            ("📈", f"{weekly_avg}%", "Weekly Average", "Across all habits", GREEN, False),
            ("🏆", str(total), "Active Habits", "Building consistency", ORANGE, False),
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
            icon_box.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px;")
            top.addWidget(icon_box)
            top.addStretch()
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

    # ─ فیلتر دسته‌بندی ───────────────────────────────────────────────────────
    def _filter_row(self):
        habits = db.get_all_habits()
        categories = ["All"] + sorted(set(h.category for h in habits))

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        for cat in categories:
            active = cat == self.selected_category
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setChecked(active)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ACCENT if active else 'transparent'};
                    color: {'white' if active else TEXT_MUTED};
                    border: 1px solid {'transparent' if active else 'rgba(255,255,255,0.12)'};
                    border-radius: 16px; padding: 6px 14px; font-size: 12px;
                }}
                QPushButton:hover {{ background: rgba(255,255,255,0.07); color: white; }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, c=cat: self._select_category(c))
            lay.addWidget(btn)

        lay.addStretch()
        return row

    def _select_category(self, category):
        self.selected_category = category
        self.refresh()

    # ─ گرید عادت‌ها ──────────────────────────────────────────────────────────
    def _habits_grid(self):
        habits = db.get_all_habits()

        if self.selected_category != "All":
            habits = [h for h in habits if h.category == self.selected_category]

        grid = QWidget()
        grid.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(grid)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        for i in range(0, len(habits), 2):
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(14)

            for h in habits[i:i+2]:
                rl.addWidget(HabitCard(h, on_toggle=self.refresh))

            if len(habits[i:i+2]) == 1:
                rl.addStretch()

            lay.addWidget(row)

        if not habits:
            empty = QLabel("هنوز عادتی ثبت نشده. یکی اضافه کن!")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent; padding: 40px;")
            lay.addWidget(empty)

        # دکمه Add Habit
        add_card = QFrame()
        add_card.setMinimumHeight(80)
        add_card.setCursor(Qt.CursorShape.PointingHandCursor)
        add_card.setStyleSheet("QFrame { background: transparent; border: 2px dashed rgba(255,255,255,0.12); border-radius: 14px; }")
        add_lay = QVBoxLayout(add_card)
        add_btn = QLabel("+ Add New Habit")
        add_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_btn.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        add_lay.addWidget(add_btn)
        lay.addWidget(add_card)

        return grid