from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QFrame, QPushButton
)
from PyQt6.QtCore import Qt

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)

PRIO_COLORS = {
    "High":   RED,
    "Medium": ORANGE,
    "Low":    GREEN,
}

CAT_COLORS = {
    "Work":   ACCENT,
    "Health": GREEN,
    "Personal": BLUE,
    "Learning": ORANGE,
}


# ─── کارت تسک ────────────────────────────────────────────────────────────────
class TaskCard(QWidget):
    def __init__(self, name, desc, category, date, time, priority, done=False, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        card = make_card(color=BG_CARD2 if not done else "#1a2a1a")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 14, 18, 14)
        lay.setSpacing(6)

        # ─ ردیف اصلی ─
        top = QHBoxLayout()
        top.setSpacing(12)

        check = QLabel("✅" if done else "⭕")
        check.setStyleSheet("font-size: 20px; background: transparent;")
        check.setFixedWidth(28)

        info = QVBoxLayout()
        info.setSpacing(3)

        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"""
            font-size: 14px; font-weight: 600;
            color: {TEXT_MUTED if done else TEXT_PRIMARY};
            background: transparent;
            {'text-decoration: line-through;' if done else ''}
        """)
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")

        info.addWidget(name_lbl)
        info.addWidget(desc_lbl)

        prio_col = PRIO_COLORS.get(priority, TEXT_MUTED)
        prio_lbl = QLabel(priority)
        prio_lbl.setStyleSheet(f"""
            font-size: 11px; font-weight: 600;
            color: {prio_col};
            background: rgba(255,255,255,0.07);
            border: 1px solid {prio_col};
            border-radius: 8px;
            padding: 3px 12px;
        """)
        prio_lbl.setFixedHeight(24)

        top.addWidget(check)
        top.addLayout(info, 1)
        top.addWidget(prio_lbl)
        lay.addLayout(top)

        # ─ تگ‌ها ─
        tags = QHBoxLayout()
        tags.setSpacing(8)
        tags.setContentsMargins(40, 0, 0, 0)

        cat_col = CAT_COLORS.get(category, ACCENT)
        cat_lbl = QLabel(category)
        cat_lbl.setStyleSheet(f"""
            font-size: 11px; color: white;
            background: {cat_col};
            border-radius: 6px; padding: 2px 10px;
        """)

        date_lbl = QLabel(f"📅 {date}")
        date_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

        time_lbl = QLabel(f"🕐 {time}")
        time_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

        tags.addWidget(cat_lbl)
        tags.addWidget(date_lbl)
        tags.addWidget(time_lbl)
        tags.addStretch()
        lay.addLayout(tags)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)


# ─── صفحه: Tasks ─────────────────────────────────────────────────────────────
class TasksPage(QWidget):
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
        layout.addWidget(self._tasks_section("Pending Tasks", self._pending_tasks()))
        layout.addWidget(self._tasks_section("Completed Tasks", self._completed_tasks()))
        layout.addStretch()

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    # ─ آمار ──────────────────────────────────────────────────────────────────
    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("✅", "6",  "Pending Tasks", "To be completed", ACCENT2, True),
            ("☑️", "4",  "Completed",     "Great progress!", GREEN,   False),
            ("📅", "5",  "Due Today",     "Focus on these",  BLUE,    False),
            ("🚩", "2",  "High Priority", "Needs attention", RED,     False),
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

    # ─ فیلتر + دکمه Add ──────────────────────────────────────────────────────
    def _filter_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        filters = ["🔽 Filter", "All Tasks", "Today", "This Week"]
        for i, f in enumerate(filters):
            btn = QPushButton(f)
            active = i == 1
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'rgba(255,255,255,0.07)' if not active else 'rgba(255,255,255,0.1)'};
                    color: {TEXT_PRIMARY if active else TEXT_MUTED};
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 16px;
                    padding: 6px 16px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,0.1);
                    color: {TEXT_PRIMARY};
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lay.addWidget(btn)

        lay.addStretch()

        add_btn = QPushButton("+ Add Task")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 16px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lay.addWidget(add_btn)

        return row

    # ─ سکشن با عنوان ─────────────────────────────────────────────────────────
    def _tasks_section(self, title, tasks_widget):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        t = QLabel(title)
        t.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(t)
        lay.addWidget(tasks_widget)
        return section

    def _pending_tasks(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        tasks = [
            ("Complete project proposal", "Write and submit the Q3 project proposal document", "Work",     "Jun 5", "2:00 PM",  "High",   False),
            ("Review pull requests",      "Code review for team members' PRs",                 "Work",     "Jun 3", "4:00 PM",  "Medium", False),
            ("Plan weekly meals",         "Prepare meal plan and grocery list",                 "Health",   "Jun 4", "10:00 AM", "Medium", False),
            ("Study algorithms",          "Complete chapter 5 of the book",                    "Learning", "Jun 6", "7:00 PM",  "Low",    False),
        ]
        for t in tasks:
            lay.addWidget(TaskCard(*t))
        return w

    def _completed_tasks(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        tasks = [
            ("Morning meditation",   "Daily mindfulness practice",     "Personal", "Jun 3", "6:00 AM",  "Low",  True),
            ("Team standup meeting", "Daily sync with the team",       "Work",     "Jun 3", "9:00 AM",  "High", True),
            ("Workout session",      "45 min gym session",             "Health",   "Jun 3", "5:00 PM",  "Medium", True),
            ("Read 30 minutes",      "Continue reading current book",  "Personal", "Jun 3", "9:00 PM",  "Low",  True),
        ]
        for t in tasks:
            lay.addWidget(TaskCard(*t))
        return w