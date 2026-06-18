from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QPushButton,
    QTextEdit, QDateEdit, QTimeEdit, QWidget
)
from PyQt6.QtCore import Qt, QDate, QTime

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2
)


# ─── استایل مشترک برای input ها ──────────────────────────────────────────────
INPUT_STYLE = f"""
    QLineEdit, QComboBox, QSpinBox {{
        background: {BG_CARD2};
        color: {TEXT_PRIMARY};
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border: 1px solid {ACCENT};
    }}
    QComboBox::drop-down {{
        border: none;
    }}
    QComboBox QAbstractItemView {{
        background: {BG_CARD2};
        color: {TEXT_PRIMARY};
        selection-background-color: {ACCENT};
    }}
"""

LABEL_STYLE = f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;"


class AddHabitDialog(QDialog):
    """دیالوگ افزودن عادت جدید. روی تایید، self.result_data پر می‌شه."""

    ICONS = ["🧘", "💪", "📚", "💧", "🎸", "📓", "🥗", "🏃", "✍️", "🎨", "💻", "🌙"]
    CATEGORIES = ["Mindfulness", "Fitness", "Health", "Personal Growth", "Skills", "Digital Wellness", "Career"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Habit")
        self.setFixedWidth(380)
        self.result_data = None

        self.setStyleSheet(f"""
            QDialog {{
                background: {BG_CARD};
                color: {TEXT_PRIMARY};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel("Add New Habit")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        # ─ نام عادت ─
        lay.addWidget(self._labeled("Habit Name", self._name_input()))

        # ─ آیکون ─
        lay.addWidget(self._labeled("Icon", self._icon_input()))

        # ─ دسته‌بندی ─
        lay.addWidget(self._labeled("Category", self._category_input()))

        # ─ تکرار ─
        freq_row = QHBoxLayout()
        freq_row.setSpacing(10)
        freq_row.addWidget(self._labeled("Frequency", self._frequency_input()), 1)
        freq_row.addWidget(self._labeled("Times / week", self._count_input()), 1)
        lay.addLayout(freq_row)

        # ─ دکمه‌ها ─
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        add_btn = QPushButton("Add Habit")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.clicked.connect(self._handle_add)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(add_btn, 1)
        lay.addLayout(btn_row)

    # ─ ابزار کمکی: لیبل + ویجت ─────────────────────────────────────────────────
    def _labeled(self, label_text, widget):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(wrapper)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(LABEL_STYLE)
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return wrapper

    # ─ ورودی‌ها ──────────────────────────────────────────────────────────────
    def _name_input(self):
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Morning Meditation")
        self.name_edit.setStyleSheet(INPUT_STYLE)
        return self.name_edit

    def _icon_input(self):
        self.icon_combo = QComboBox()
        self.icon_combo.addItems(self.ICONS)
        self.icon_combo.setStyleSheet(INPUT_STYLE)
        return self.icon_combo

    def _category_input(self):
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.CATEGORIES)
        self.category_combo.setStyleSheet(INPUT_STYLE)
        return self.category_combo

    def _frequency_input(self):
        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["Daily", "Weekly"])
        self.freq_combo.setStyleSheet(INPUT_STYLE)
        self.freq_combo.currentTextChanged.connect(self._on_freq_changed)
        return self.freq_combo

    def _count_input(self):
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 7)
        self.count_spin.setValue(7)
        self.count_spin.setEnabled(False)  # چون پیش‌فرض Daily است
        self.count_spin.setStyleSheet(INPUT_STYLE)
        return self.count_spin

    def _on_freq_changed(self, text):
        if text == "Daily":
            self.count_spin.setValue(7)
            self.count_spin.setEnabled(False)
        else:
            self.count_spin.setValue(3)
            self.count_spin.setEnabled(True)

    # ─ تایید ─────────────────────────────────────────────────────────────────
    def _handle_add(self):
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setStyleSheet(INPUT_STYLE + f"QLineEdit {{ border: 1px solid #e05c5c; }}")
            return

        self.result_data = {
            "name": name,
            "icon": self.icon_combo.currentText(),
            "category": self.category_combo.currentText(),
            "frequency_type": self.freq_combo.currentText().lower(),
            "frequency_count": self.count_spin.value(),
        }
        self.accept()


# ════════════════════════════════════════════════════════════════════════════
class AddTaskDialog(QDialog):
    """دیالوگ افزودن تسک جدید. روی تایید، self.result_data پر می‌شه."""

    CATEGORIES = ["Work", "Personal", "Health", "Learning", "Fitness", "Wellness"]
    PRIORITIES = ["High", "Medium", "Low"]

    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task  # اگه None باشه = حالت Add, اگه مقدار داشته باشه = حالت Edit
        is_edit = task is not None

        self.setWindowTitle("Edit Task" if is_edit else "Add New Task")
        self.setFixedWidth(380)
        self.result_data = None

        self.setStyleSheet(f"""
            QDialog {{
                background: {BG_CARD};
                color: {TEXT_PRIMARY};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel("Edit Task" if is_edit else "Add New Task")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        # ─ نام تسک ─
        lay.addWidget(self._labeled("Task Name", self._name_input()))

        # ─ توضیحات ─
        lay.addWidget(self._labeled("Description", self._desc_input()))

        # ─ دسته‌بندی + اولویت ─
        row1 = QHBoxLayout()
        row1.setSpacing(10)
        row1.addWidget(self._labeled("Category", self._category_input()), 1)
        row1.addWidget(self._labeled("Priority", self._priority_input()), 1)
        lay.addLayout(row1)

        # ─ تاریخ + زمان ─
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        row2.addWidget(self._labeled("Due Date", self._date_input()), 1)
        row2.addWidget(self._labeled("Due Time", self._time_input()), 1)
        lay.addLayout(row2)

        # ─ اگه حالت Edit باشه، فیلدها رو با مقدار فعلی پر کن ─
        if is_edit:
            self._fill_from_task(task)

        # ─ دکمه‌ها ─
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        add_btn = QPushButton("Save Changes" if is_edit else "Add Task")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.clicked.connect(self._handle_add)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(add_btn, 1)
        lay.addLayout(btn_row)

    # ─ ابزار کمکی: لیبل + ویجت ─────────────────────────────────────────────────
    def _labeled(self, label_text, widget):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(wrapper)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(LABEL_STYLE)
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return wrapper

    # ─ ورودی‌ها ──────────────────────────────────────────────────────────────
    def _name_input(self):
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Complete project proposal")
        self.name_edit.setStyleSheet(INPUT_STYLE)
        return self.name_edit

    def _desc_input(self):
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Short description...")
        self.desc_edit.setStyleSheet(INPUT_STYLE)
        return self.desc_edit

    def _category_input(self):
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.CATEGORIES)
        self.category_combo.setStyleSheet(INPUT_STYLE)
        return self.category_combo

    def _priority_input(self):
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(self.PRIORITIES)
        self.priority_combo.setStyleSheet(INPUT_STYLE)
        return self.priority_combo

    def _date_input(self):
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setStyleSheet(INPUT_STYLE)
        return self.date_edit

    def _time_input(self):
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(12, 0))
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet(INPUT_STYLE)
        return self.time_edit

    # ─ تایید ─────────────────────────────────────────────────────────────────
    def _handle_add(self):
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setStyleSheet(INPUT_STYLE + f"QLineEdit {{ border: 1px solid #e05c5c; }}")
            return

        self.result_data = {
            "name": name,
            "description": self.desc_edit.text().strip(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_combo.currentText(),
            "due_date": self.date_edit.date().toString("yyyy-MM-dd"),
            "due_time": self.time_edit.time().toString("HH:mm"),
        }
        self.accept()

    # ─ پر کردن فیلدها از یه تسک موجود (حالت Edit) ───────────────────────────
    def _fill_from_task(self, task):
        self.name_edit.setText(task.name)
        self.desc_edit.setText(task.description or "")

        idx = self.category_combo.findText(task.category)
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)

        idx = self.priority_combo.findText(task.priority)
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)

        if task.due_date:
            self.date_edit.setDate(QDate.fromString(task.due_date, "yyyy-MM-dd"))

        if task.due_time:
            self.time_edit.setTime(QTime.fromString(task.due_time, "HH:mm"))


# ════════════════════════════════════════════════════════════════════════════
class AddGoalDialog(QDialog):
    """دیالوگ افزودن/ویرایش هدف. روی تایید، self.result_data پر می‌شه."""

    ICONS = ["🎯", "🚀", "📈", "🏃", "🌍", "📚", "💻", "🎨", "💪", "🧘", "💰", "🎓"]
    CATEGORIES = ["Learning", "Fitness", "Career", "Personal", "Health", "Finance"]

    def __init__(self, parent=None, goal=None):
        super().__init__(parent)
        self.goal = goal
        is_edit = goal is not None

        self.setWindowTitle("Edit Goal" if is_edit else "Add New Goal")
        self.setFixedWidth(380)
        self.result_data = None

        self.setStyleSheet(f"""
            QDialog {{
                background: {BG_CARD};
                color: {TEXT_PRIMARY};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel("Edit Goal" if is_edit else "Add New Goal")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        # ─ نام هدف ─
        lay.addWidget(self._labeled("Goal Name", self._name_input()))

        # ─ توضیحات ─
        lay.addWidget(self._labeled("Description", self._desc_input()))

        # ─ آیکون + دسته‌بندی ─
        row1 = QHBoxLayout()
        row1.setSpacing(10)
        row1.addWidget(self._labeled("Icon", self._icon_input()), 1)
        row1.addWidget(self._labeled("Category", self._category_input()), 1)
        lay.addLayout(row1)

        # ─ مهلت ─
        lay.addWidget(self._labeled("Deadline", self._deadline_input()))

        if is_edit:
            self._fill_from_goal(goal)

        # ─ دکمه‌ها ─
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        add_btn = QPushButton("Save Changes" if is_edit else "Add Goal")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.clicked.connect(self._handle_add)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(add_btn, 1)
        lay.addLayout(btn_row)

    # ─ ابزار کمکی: لیبل + ویجت ─────────────────────────────────────────────────
    def _labeled(self, label_text, widget):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(wrapper)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(LABEL_STYLE)
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return wrapper

    # ─ ورودی‌ها ──────────────────────────────────────────────────────────────
    def _name_input(self):
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Learn Full-Stack Web Development")
        self.name_edit.setStyleSheet(INPUT_STYLE)
        return self.name_edit

    def _desc_input(self):
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Short description...")
        self.desc_edit.setStyleSheet(INPUT_STYLE)
        return self.desc_edit

    def _icon_input(self):
        self.icon_combo = QComboBox()
        self.icon_combo.addItems(self.ICONS)
        self.icon_combo.setStyleSheet(INPUT_STYLE)
        return self.icon_combo

    def _category_input(self):
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.CATEGORIES)
        self.category_combo.setStyleSheet(INPUT_STYLE)
        return self.category_combo

    def _deadline_input(self):
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addMonths(3))
        self.deadline_edit.setDisplayFormat("yyyy-MM-dd")
        self.deadline_edit.setStyleSheet(INPUT_STYLE)
        return self.deadline_edit

    # ─ تایید ─────────────────────────────────────────────────────────────────
    def _handle_add(self):
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setStyleSheet(INPUT_STYLE + f"QLineEdit {{ border: 1px solid #e05c5c; }}")
            return

        self.result_data = {
            "name": name,
            "description": self.desc_edit.text().strip(),
            "icon": self.icon_combo.currentText(),
            "category": self.category_combo.currentText(),
            "deadline": self.deadline_edit.date().toString("yyyy-MM-dd"),
        }
        self.accept()

    # ─ پر کردن فیلدها از یه هدف موجود (حالت Edit) ───────────────────────────
    def _fill_from_goal(self, goal):
        self.name_edit.setText(goal.name)
        self.desc_edit.setText(goal.description or "")

        idx = self.icon_combo.findText(goal.icon)
        if idx >= 0:
            self.icon_combo.setCurrentIndex(idx)

        idx = self.category_combo.findText(goal.category)
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)

        if goal.deadline:
            self.deadline_edit.setDate(QDate.fromString(goal.deadline, "yyyy-MM-dd"))


# ════════════════════════════════════════════════════════════════════════════
class AddMilestoneDialog(QDialog):
    """دیالوگ کوچک برای افزودن یه مایلستون به یه هدف."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Milestone")
        self.setFixedWidth(320)
        self.result_data = None

        self.setStyleSheet(f"""
            QDialog {{
                background: {BG_CARD};
                color: {TEXT_PRIMARY};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel("Add Milestone")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Complete React fundamentals")
        self.name_edit.setStyleSheet(INPUT_STYLE)
        lay.addWidget(self.name_edit)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        add_btn = QPushButton("Add")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 0;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        add_btn.clicked.connect(self._handle_add)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(add_btn, 1)
        lay.addLayout(btn_row)

    def _handle_add(self):
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setStyleSheet(INPUT_STYLE + f"QLineEdit {{ border: 1px solid #e05c5c; }}")
            return
        self.result_data = {"name": name}
        self.accept()


# ════════════════════════════════════════════════════════════════════════════
class EditSessionDialog(QDialog):
    """دیالوگ ویرایش اسم و دسته یه session."""

    CATEGORIES = ["Study", "Work", "Fitness", "Personal", "Other"]

    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Edit Session")
        self.setFixedWidth(320)
        self.result_data = None

        self.setStyleSheet(f"QDialog {{ background: {BG_CARD}; color: {TEXT_PRIMARY}; }}")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel("Edit Session")
        title.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        dur_lbl = QLabel(f"Duration: {session.duration_str}")
        dur_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        lay.addWidget(dur_lbl)

        INPUT = f"""
            QLineEdit, QComboBox {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; padding: 8px 12px; font-size: 13px;
            }}
            QComboBox QAbstractItemView {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                selection-background-color: {ACCENT};
            }}
        """

        name_lbl = QLabel("Session Name")
        name_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        self.name_edit = QLineEdit(session.name)
        self.name_edit.setStyleSheet(INPUT)
        lay.addWidget(name_lbl)
        lay.addWidget(self.name_edit)

        cat_lbl = QLabel("Category")
        cat_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(self.CATEGORIES)
        idx = self.cat_combo.findText(session.category)
        if idx >= 0:
            self.cat_combo.setCurrentIndex(idx)
        self.cat_combo.setStyleSheet(INPUT)
        lay.addWidget(cat_lbl)
        lay.addWidget(self.cat_combo)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px; padding: 10px 0; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white; border: none;
                border-radius: 10px; padding: 10px 0;
                font-size: 13px; font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        save_btn.clicked.connect(self._handle_save)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(save_btn, 1)
        lay.addLayout(btn_row)

    def _handle_save(self):
        name = self.name_edit.text().strip() or self.cat_combo.currentText()
        self.result_data = {
            "name": name,
            "category": self.cat_combo.currentText(),
        }
        self.accept()