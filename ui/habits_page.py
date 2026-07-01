from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)
from database import db_manager as db
from core.streak_engine import (
    daily_streak, best_daily_streak,
    weekly_streak, week_status, predict_streak_break
)
from ui.dialogs import AddHabitDialog


# ─── WeekBar ──────────────────────────────────────────────────────────────────
class WeekBar(QWidget):
    def __init__(self, daily_log=None, color=GREEN, parent=None):
        super().__init__(parent)
        # daily_log: لیست ۷ تایی True/False برای هر روز هفته
        self.daily_log = daily_log or [False] * 7
        self.color     = color
        self.setFixedHeight(10)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w   = self.width()
        gap = 6
        n   = 7
        bw  = (w - gap * (n - 1)) / n
        for i, done in enumerate(self.daily_log):
            x = i * (bw + gap)
            p.setBrush(QColor(self.color) if done else QColor(BG_CARD2))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(int(x), 0, int(bw), 10, 5, 5)


# ─── HabitCard ────────────────────────────────────────────────────────────────
class HabitCard(QWidget):
    def __init__(self, habit, on_change, parent=None):
        super().__init__(parent)
        self.habit     = habit
        self.on_change = on_change
        self.setStyleSheet("background: transparent;")

        # داده از streak_engine
        ws             = week_status(habit.id)
        done_today     = db.is_habit_done_today(habit.id)
        cur_streak     = daily_streak(habit.id)
        best_str       = best_daily_streak(habit.id)
        w_streak       = weekly_streak(habit.id)
        prediction     = predict_streak_break(habit.id)
        daily_log      = ws.get("daily_log", [False]*7)
        done_week      = ws.get("done", 0)
        total_week     = ws.get("target", habit.frequency_count)
        on_track       = ws.get("on_track", True)

        freq_text = "Daily" if habit.frequency_type == "daily" else f"{habit.frequency_count}x / week"

        # رنگ پیش‌بینی
        pred_color = {
            "on_track": GREEN,
            "at_risk":  ORANGE,
            "broken":   RED,
        }.get(prediction, TEXT_MUTED)

        card = make_card(color="#1a2a1a" if done_today else BG_CARD)
        card.setMinimumHeight(180)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        # ─ ردیف بالا ─
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

        # نشانه پیش‌بینی
        if prediction == "at_risk":
            warn = QLabel("⚠ At Risk")
            warn.setStyleSheet(f"font-size: 11px; color: {ORANGE}; background: transparent;")
            tags.addWidget(warn)
        elif prediction == "broken":
            warn = QLabel("✕ Broken")
            warn.setStyleSheet(f"font-size: 11px; color: {RED}; background: transparent;")
            tags.addWidget(warn)

        tags.addStretch()
        info.addWidget(name_lbl)
        info.addLayout(tags)

        # دکمه‌های action
        actions = QHBoxLayout()
        actions.setSpacing(4)

        self.check_btn = QPushButton("✅" if done_today else "⭕")
        self.check_btn.setFixedSize(32, 32)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.setStyleSheet("QPushButton { font-size: 20px; background: transparent; border: none; } QPushButton:hover { background: rgba(255,255,255,0.08); border-radius: 8px; }")
        self.check_btn.clicked.connect(self._handle_toggle)

        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(28, 28)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("QPushButton { font-size: 13px; background: transparent; border: none; } QPushButton:hover { background: rgba(255,255,255,0.1); border-radius: 8px; }")
        edit_btn.clicked.connect(self._handle_edit)

        del_btn = QPushButton("🗑️")
        del_btn.setFixedSize(28, 28)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("QPushButton { font-size: 13px; background: transparent; border: none; } QPushButton:hover { background: rgba(224,92,92,0.2); border-radius: 8px; }")
        del_btn.clicked.connect(self._handle_delete)

        actions.addWidget(self.check_btn)
        actions.addWidget(edit_btn)
        actions.addWidget(del_btn)

        top.addWidget(icon_box)
        top.addSpacing(10)
        top.addLayout(info, 1)
        top.addLayout(actions)
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
        lay.addWidget(WeekBar(daily_log, GREEN))

        # ─ Streak ─
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: rgba(255,255,255,0.06);")
        lay.addWidget(sep)

        streak_row = QHBoxLayout()

        cur_col = QVBoxLayout()
        cur_lbl = QLabel("Daily Streak")
        cur_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        cur_val = QLabel(f"🔥 {cur_streak} days")
        cur_val.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {ORANGE}; background: transparent;")
        cur_col.addWidget(cur_lbl)
        cur_col.addWidget(cur_val)

        week_str_col = QVBoxLayout()
        week_str_col.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        wsl = QLabel("Weekly Streak")
        wsl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        wsl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        wsv = QLabel(f"📅 {w_streak} weeks")
        wsv.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {BLUE}; background: transparent;")
        wsv.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        week_str_col.addWidget(wsl)
        week_str_col.addWidget(wsv)

        best_col = QVBoxLayout()
        best_col.setAlignment(Qt.AlignmentFlag.AlignRight)
        best_lbl = QLabel("Best Streak")
        best_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        best_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        best_val = QLabel(f"{best_str} days")
        best_val.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        best_val.setAlignment(Qt.AlignmentFlag.AlignRight)
        best_col.addWidget(best_lbl)
        best_col.addWidget(best_val)

        streak_row.addLayout(cur_col)
        streak_row.addStretch()
        streak_row.addLayout(week_str_col)
        streak_row.addStretch()
        streak_row.addLayout(best_col)
        lay.addLayout(streak_row)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

    def _handle_toggle(self):
        db.toggle_habit_today(self.habit.id)
        self.on_change()

    def _handle_edit(self):
        dialog = AddHabitDialog(self, habit=self.habit)
        if dialog.exec():
            data = dialog.result_data
            db.update_habit(
                self.habit.id,
                data["name"], data["icon"], data["category"],
                data["frequency_type"], data["frequency_count"]
            )
            self.on_change()

    def _handle_delete(self):
        reply = QMessageBox.question(
            self, "Delete Habit",
            f"Are you sure you want to delete '{self.habit.name}'?\nThis will also delete all its history.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_habit(self.habit.id)
            self.on_change()


# ─── HabitsPage ───────────────────────────────────────────────────────────────
class HabitsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        self.selected_category = "All"

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

        layout.addWidget(self._stats_row())
        layout.addWidget(self._filter_row())
        layout.addWidget(self._habits_grid())
        layout.addStretch()

        self.scroll.setWidget(content)

    def _stats_row(self):
        habits     = db.get_all_habits()
        total      = len(habits)
        done_today = sum(1 for h in habits if db.is_habit_done_today(h.id))
        today_pct  = round(done_today / total * 100) if total else 0

        # طولانی‌ترین streak
        best_per   = [(h, best_daily_streak(h.id)) for h in habits]
        top_habit, longest = max(best_per, key=lambda x: x[1]) if best_per else (None, 0)
        longest_name = top_habit.name if top_habit and longest > 0 else "—"

        # میانگین هفتگی
        if habits:
            week_pcts = []
            for h in habits:
                ws = week_status(h.id)
                t  = ws.get("target", h.frequency_count)
                d  = ws.get("done", 0)
                week_pcts.append(min(d / t, 1) * 100 if t else 0)
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
            ("🔥", str(longest),    "Longest Streak",      longest_name,                    ORANGE, False),
            ("📈", f"{weekly_avg}%","Weekly Average",      "Across all habits",              GREEN,  False),
            ("🏆", str(total),      "Active Habits",       "Building consistency",           ORANGE, False),
        ]

        for icon, val, title, sub, col, highlight in items:
            card = make_card(color="#1a1535" if highlight else BG_CARD)
            card.setMinimumHeight(120)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(18, 16, 18, 16)
            cl.setSpacing(6)
            top = QHBoxLayout()
            ib = QLabel(icon)
            ib.setFixedSize(40, 40)
            ib.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ib.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px;")
            top.addWidget(ib)
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

    def _filter_row(self):
        habits     = db.get_all_habits()
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
                rl.addWidget(HabitCard(h, on_change=self.refresh))
            if len(habits[i:i+2]) == 1:
                rl.addStretch()
            lay.addWidget(row)

        if not habits:
            empty = QLabel("هنوز عادتی ثبت نشده. یکی اضافه کن!")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent; padding: 40px;")
            lay.addWidget(empty)

        # دکمه Add
        add_card = QFrame()
        add_card.setMinimumHeight(80)
        add_card.setCursor(Qt.CursorShape.PointingHandCursor)
        add_card.setStyleSheet("QFrame { background: transparent; border: 2px dashed rgba(255,255,255,0.12); border-radius: 14px; }")
        add_lay = QVBoxLayout(add_card)
        add_lbl = QLabel("+ Add New Habit")
        add_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_lbl.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        add_lay.addWidget(add_lbl)
        add_card.mousePressEvent = lambda e: self._open_add_dialog()
        lay.addWidget(add_card)

        return grid

    def _open_add_dialog(self):
        dialog = AddHabitDialog(self)
        if dialog.exec():
            data = dialog.result_data
            db.add_habit(
                data["name"], data["icon"], data["category"],
                data["frequency_type"], data["frequency_count"]
            )
            self.refresh()