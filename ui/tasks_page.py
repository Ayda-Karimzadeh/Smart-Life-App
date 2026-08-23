from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QFrame, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import date, datetime

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
)
from ui.dialogs import AddTaskDialog
from core.language_manager import tr

PRIO_COLORS = {
    "High":   RED,
    "Medium": ORANGE,
    "Low":    GREEN,
}

CAT_COLORS = {
    "Work":     ACCENT,
    "Health":   GREEN,
    "Personal": BLUE,
    "Learning": ORANGE,
    "Fitness":  RED,
    "Wellness": ACCENT2,
}


# ─── کارت تسک ────────────────────────────────────────────────────────────────
class TaskCard(QWidget):
    """کارت یه تسک. کلیک روی دایره چک، وضعیت done رو toggle می‌کنه."""

    def __init__(self, task, on_toggle, parent=None):
        super().__init__(parent)
        self.task = task
        self.on_toggle = on_toggle
        self.setStyleSheet("background: transparent;")

        done = task.done
        card = make_card(color=BG_CARD2 if not done else "#1a2a1a")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 14, 18, 14)
        lay.setSpacing(6)

        # ─ ردیف اصلی ─
        top = QHBoxLayout()
        top.setSpacing(12)

        self.check_btn = QPushButton("✅" if done else "⭕")
        self.check_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.08);
                border-radius: 8px;
            }
        """)
        self.check_btn.setFixedSize(28, 28)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.clicked.connect(self._handle_toggle)

        info = QVBoxLayout()
        info.setSpacing(3)

        name_lbl = QLabel(task.name)
        name_lbl.setStyleSheet(f"""
            font-size: 14px; font-weight: 600;
            color: {TEXT_MUTED if done else TEXT_PRIMARY};
            background: transparent;
            {'text-decoration: line-through;' if done else ''}
        """)
        info.addWidget(name_lbl)

        if task.description:
            desc_lbl = QLabel(task.description)
            desc_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            info.addWidget(desc_lbl)

        prio_col = PRIO_COLORS.get(task.priority, TEXT_MUTED)
        prio_text = tr(f"prio_{task.priority.lower()}")
        prio_lbl = QLabel(prio_text)
        prio_lbl.setStyleSheet(f"""
            font-size: 11px; font-weight: 600;
            color: {prio_col};
            background: rgba(255,255,255,0.07);
            border: 1px solid {prio_col};
            border-radius: 8px;
            padding: 3px 12px;
        """)
        prio_lbl.setFixedHeight(24)

        # دکمه ویرایش
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(28, 28)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.08);
                border-radius: 8px;
            }
        """)
        edit_btn.clicked.connect(self._handle_edit)

        # دکمه حذف
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(28, 28)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(224,92,92,0.15);
                border-radius: 8px;
            }
        """)
        delete_btn.clicked.connect(self._handle_delete)

        top.addWidget(self.check_btn)
        top.addLayout(info, 1)
        top.addWidget(prio_lbl)
        top.addWidget(edit_btn)
        top.addWidget(delete_btn)
        lay.addLayout(top)

        # ─ تگ‌ها ─
        tags = QHBoxLayout()
        tags.setSpacing(8)
        tags.setContentsMargins(40, 0, 0, 0)

        cat_col = CAT_COLORS.get(task.category, ACCENT)
        cat_text = tr(f"cat_{task.category.lower()}")
        cat_lbl = QLabel(cat_text)
        cat_lbl.setStyleSheet(f"""
            font-size: 11px; color: white;
            background: {cat_col};
            border-radius: 6px; padding: 2px 10px;
        """)
        tags.addWidget(cat_lbl)

        if task.due_date:
            date_lbl = QLabel(f"📅 {task.due_date}")
            date_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            tags.addWidget(date_lbl)

        if task.due_time:
            time_lbl = QLabel(f"🕐 {task.due_time}")
            time_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            tags.addWidget(time_lbl)

        tags.addStretch()
        lay.addLayout(tags)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

    def _handle_toggle(self):
        task_repo.toggle_task(self.task.id)
        self.on_toggle()

    def _handle_edit(self):
        dialog = AddTaskDialog(self, task=self.task)
        if dialog.exec():
            data = dialog.result_data
            task_repo.update_task(
                task_id=self.task.id,
                name=data["name"],
                description=data["description"],
                category=data["category"],
                priority=data["priority"],
                due_date=data["due_date"],
                due_time=data["due_time"],
            )
            self.on_toggle()  # refresh

    def _handle_delete(self):
        reply = QMessageBox.question(
            self, tr("delete_task"),
            tr("delete_task_confirm").format(name=self.task.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            task_repo.delete_task(self.task.id)
            self.on_toggle()  # refresh


# ─── صفحه: Tasks ─────────────────────────────────────────────────────────────
class TasksPage(QWidget):

    # نگاشت کلید انگلیسیِ ثابت (منطق داخلی فیلتر) به کلید ترجمه برای نمایش
    FILTER_TR_KEYS = {
        "All Tasks": "filter_all_tasks",
        "Today": "filter_today",
        "This Week": "filter_this_week",
    }

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.active_filter = "All Tasks"  # All Tasks / Today / This Week
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

        pending = self._filtered_tasks(done=False)
        completed = self._filtered_tasks(done=True)

        layout.addWidget(self._tasks_section(f"{tr('pending_tasks')} ({len(pending)})", pending))
        layout.addWidget(self._tasks_section(f"{tr('completed')} ({len(completed)})", completed))
        layout.addStretch()

        self.scroll.setWidget(content)

    # ─ فیلتر بر اساس Today / This Week ──────────────────────────────────────────
    def _filtered_tasks(self, done):
        tasks = task_repo.get_all_tasks(done=done)

        if self.active_filter == "Today":
            today = date.today().isoformat()
            tasks = [t for t in tasks if t.due_date == today]
        elif self.active_filter == "This Week":
            today = date.today()
            from datetime import timedelta
            week_end = today + timedelta(days=7)
            tasks = [
                t for t in tasks
                if t.due_date and today.isoformat() <= t.due_date <= week_end.isoformat()
            ]

        return tasks

    # ─ آمار ──────────────────────────────────────────────────────────────────
    def _stats_row(self):
        all_tasks = task_repo.get_all_tasks()
        pending = [t for t in all_tasks if not t.done]
        completed = [t for t in all_tasks if t.done]

        today = date.today().isoformat()
        due_today = [t for t in all_tasks if t.due_date == today and not t.done]
        high_prio = [t for t in pending if t.priority == "High"]

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("✅", str(len(pending)),   tr("tasks_pending"), tr("to_be_completed"), ACCENT2, True),
            ("☑️", str(len(completed)), tr("completed"),     tr("great_progress"),  GREEN,   False),
            ("📅", str(len(due_today)), tr("due_today"),     tr("focus_on_these"),  BLUE,    False),
            ("🚩", str(len(high_prio)), tr("prio_high") + " " + tr("priority"), tr("needs_attention"), RED, False),
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
            icon_box.setStyleSheet("""
                font-size: 20px;
                background: rgba(255,255,255,0.07);
                border-radius: 10px;
                margin-bottom: 6px;
            """)
            top.addWidget(icon_box)
            top.addStretch()

            val_lbl = QLabel(val)
            val_lbl.setMinimumHeight(40)
            val_lbl.setStyleSheet(f"font-size: 30px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent; padding-top: 6px;")
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

        filters = ["All Tasks", "Today", "This Week"]
        for f in filters:
            active = f == self.active_filter
            btn = QPushButton(tr(self.FILTER_TR_KEYS[f]))
            btn.setCheckable(True)
            btn.setChecked(active)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ACCENT if active else 'rgba(255,255,255,0.07)'};
                    color: {'white' if active else TEXT_MUTED};
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 16px;
                    padding: 6px 16px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,0.1);
                    color: white;
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, name=f: self._select_filter(name))
            lay.addWidget(btn)

        lay.addStretch()

        add_btn = QPushButton("+ " + tr("add_task_btn"))
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
        add_btn.clicked.connect(self._open_add_dialog)
        lay.addWidget(add_btn)

        return row

    def _select_filter(self, name):
        self.active_filter = name
        self.refresh()

    # ─ باز کردن دیالوگ افزودن تسک ────────────────────────────────────────────
    def _open_add_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            data = dialog.result_data
            task_repo.add_task(
                name=data["name"],
                description=data["description"],
                category=data["category"],
                priority=data["priority"],
                due_date=data["due_date"],
                due_time=data["due_time"],
            )
            self.refresh()

    # ─ سکشن با عنوان ─────────────────────────────────────────────────────────
    def _tasks_section(self, title, tasks):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        t = QLabel(title)
        t.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(t)

        if not tasks:
            empty_container = QWidget()
            empty_container.setStyleSheet("background: transparent;")
            empty_lay = QVBoxLayout(empty_container)
            empty_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lay.setSpacing(8)
            empty_lay.setContentsMargins(20, 30, 20, 30)

            icon = QLabel("📋")
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet("font-size: 32px; background: transparent;")
            empty_lay.addWidget(icon)

            empty = QLabel(tr("no_tasks_add"))
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
            lay.addWidget(empty_container)
        else:
            for task in tasks:
                lay.addWidget(TaskCard(task, on_toggle=self.refresh))

        return section