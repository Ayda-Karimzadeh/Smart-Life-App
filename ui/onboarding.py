from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QStackedWidget,
    QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from assets.style import (
    BG_MAIN, BG_CARD, BG_CARD2,
    TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE
)
from database.repository import habit_repo, goal_repo, settings_repo


# ─── داده‌های پیشنهادی ────────────────────────────────────────────────────────
SUGGESTED_HABITS = [
    ("🧘", "Morning Meditation", "Mindfulness", "daily",  7),
    ("💪", "Exercise",           "Fitness",     "weekly", 3),
    ("📚", "Reading",            "Personal Growth", "daily", 7),
    ("💧", "Drink 8 Glasses",   "Health",      "daily",  7),
    ("🌙", "Sleep by 11 PM",    "Health",      "daily",  7),
    ("🎸", "Practice a Skill",  "Skills",      "weekly", 3),
    ("📓", "Journaling",        "Mindfulness", "daily",  7),
    ("🏃", "Morning Walk",      "Fitness",     "daily",  7),
]

SUGGESTED_GOALS = [
    ("🎯", "Learn Something New",    "Learning",  90),
    ("💪", "Get Fit",                "Fitness",   180),
    ("💰", "Save Money",             "Finance",   365),
    ("📖", "Read 12 Books",          "Personal",  365),
    ("🚀", "Build a Side Project",   "Career",    180),
    ("🌍", "Learn a New Language",   "Learning",  365),
]

BTN_STYLE = lambda color, hover: f"""
    QPushButton {{
        background: {color}; color: white; border: none;
        border-radius: 12px; padding: 12px 28px;
        font-size: 14px; font-weight: 600;
    }}
    QPushButton:hover {{ background: {hover}; }}
"""

GHOST_BTN = f"""
    QPushButton {{
        background: transparent; color: {TEXT_MUTED};
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px; padding: 12px 28px; font-size: 14px;
    }}
    QPushButton:hover {{ background: rgba(255,255,255,0.05); color: white; }}
"""

CARD_CHECK_STYLE = lambda selected: f"""
    QFrame {{
        background: {'rgba(124,92,191,0.25)' if selected else BG_CARD2};
        border: 2px solid {'%s' % ACCENT if selected else 'rgba(255,255,255,0.08)'};
        border-radius: 12px;
    }}
"""


# ─── صفحه ۱: خوش‌آمدگویی ────────────────────────────────────────────────────
class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(20)
        lay.setContentsMargins(60, 40, 60, 40)

        icon = QLabel("✦")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(f"font-size: 56px; color: {ACCENT2}; background: transparent;")
        lay.addWidget(icon)

        title = QLabel("Welcome to\nSmart Life Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 28px; font-weight: bold;
            color: {TEXT_PRIMARY}; background: transparent;
            line-height: 1.4;
        """)
        lay.addWidget(title)

        sub = QLabel(
            "یه داشبورد شخصی برای مدیریت عادت‌ها، اهداف و وقتت.\n"
            "بذار با هم شروع کنیم — فقط ۳ مرحله‌ست!"
        )
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(sub)

        # اسم کاربر
        lay.addSpacing(10)
        name_lbl = QLabel("اسمت چیه؟")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(name_lbl)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("مثلاً: Alex")
        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_edit.setMaximumWidth(300)
        self.name_edit.setStyleSheet(f"""
            QLineEdit {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                border: 2px solid rgba(255,255,255,0.1);
                border-radius: 10px; padding: 10px 16px;
                font-size: 15px;
            }}
            QLineEdit:focus {{ border: 2px solid {ACCENT}; }}
        """)
        lay.addWidget(self.name_edit, alignment=Qt.AlignmentFlag.AlignHCenter)

    def get_name(self):
        return self.name_edit.text().strip() or "Alex"


# ─── صفحه ۲: انتخاب عادت‌ها ─────────────────────────────────────────────────
class HabitsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.selected = set()  # ایندکس‌های انتخاب‌شده

        lay = QVBoxLayout(self)
        lay.setContentsMargins(40, 30, 40, 30)
        lay.setSpacing(16)

        title = QLabel("چه عادت‌هایی می‌خوای شروع کنی؟")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        sub = QLabel("حداقل یکی انتخاب کن — بعداً می‌تونی تغییرشون بدی")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(sub)

        # گرید عادت‌ها
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_lay = QVBoxLayout(grid_widget)
        grid_lay.setSpacing(10)
        grid_lay.setContentsMargins(0, 0, 0, 0)

        self.cards = []
        for row in range(0, len(SUGGESTED_HABITS), 2):
            row_w = QWidget()
            row_w.setStyleSheet("background: transparent;")
            row_lay = QHBoxLayout(row_w)
            row_lay.setSpacing(10)
            row_lay.setContentsMargins(0, 0, 0, 0)

            for col in range(2):
                idx = row + col
                if idx >= len(SUGGESTED_HABITS):
                    row_lay.addStretch()
                    break
                icon, name, cat, _, _ = SUGGESTED_HABITS[idx]
                card = self._make_habit_card(idx, icon, name, cat)
                row_lay.addWidget(card)
                self.cards.append(card)

            grid_lay.addWidget(row_w)

        scroll.setWidget(grid_widget)
        lay.addWidget(scroll)

    def _make_habit_card(self, idx, icon, name, cat):
        frame = QFrame()
        frame.setStyleSheet(CARD_CHECK_STYLE(False))
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        frame.setFixedHeight(64)

        lay = QHBoxLayout(frame)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 22px; background: transparent;")
        icon_lbl.setFixedWidth(30)

        info = QVBoxLayout()
        info.setSpacing(2)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        cat_lbl = QLabel(cat)
        cat_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        info.addWidget(name_lbl)
        info.addWidget(cat_lbl)

        check = QLabel("")
        check.setFixedSize(22, 22)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check.setStyleSheet(f"""
            font-size: 14px;
            background: rgba(255,255,255,0.05);
            border-radius: 11px;
            border: 1px solid rgba(255,255,255,0.15);
        """)

        lay.addWidget(icon_lbl)
        lay.addLayout(info, 1)
        lay.addWidget(check)

        frame.mousePressEvent = lambda e, i=idx, f=frame, c=check: self._toggle(i, f, c)
        return frame

    def _toggle(self, idx, frame, check):
        if idx in self.selected:
            self.selected.discard(idx)
            frame.setStyleSheet(CARD_CHECK_STYLE(False))
            check.setText("")
            check.setStyleSheet(f"""
                font-size: 14px; background: rgba(255,255,255,0.05);
                border-radius: 11px; border: 1px solid rgba(255,255,255,0.15);
            """)
        else:
            self.selected.add(idx)
            frame.setStyleSheet(CARD_CHECK_STYLE(True))
            check.setText("✓")
            check.setStyleSheet(f"""
                font-size: 14px; color: white;
                background: {ACCENT}; border-radius: 11px; border: none;
            """)

    def get_selected_habits(self):
        return [SUGGESTED_HABITS[i] for i in sorted(self.selected)]


# ─── صفحه ۳: انتخاب هدف ─────────────────────────────────────────────────────
class GoalsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.selected = set()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(40, 30, 40, 30)
        lay.setSpacing(16)

        title = QLabel("یه هدف بزرگ داری؟")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        sub = QLabel("می‌تونی بیشتر از یکی انتخاب کنی یا رد کنی")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(sub)

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_lay = QVBoxLayout(grid_widget)
        grid_lay.setSpacing(10)
        grid_lay.setContentsMargins(0, 0, 0, 0)

        for row in range(0, len(SUGGESTED_GOALS), 2):
            row_w = QWidget()
            row_w.setStyleSheet("background: transparent;")
            row_lay = QHBoxLayout(row_w)
            row_lay.setSpacing(10)
            row_lay.setContentsMargins(0, 0, 0, 0)

            for col in range(2):
                idx = row + col
                if idx >= len(SUGGESTED_GOALS):
                    row_lay.addStretch()
                    break
                icon, name, cat, days = SUGGESTED_GOALS[idx]
                card = self._make_goal_card(idx, icon, name, cat, days)
                row_lay.addWidget(card)

            grid_lay.addWidget(row_w)

        lay.addWidget(grid_widget)
        lay.addStretch()

    def _make_goal_card(self, idx, icon, name, cat, days):
        frame = QFrame()
        frame.setStyleSheet(CARD_CHECK_STYLE(False))
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        frame.setFixedHeight(70)

        lay = QHBoxLayout(frame)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 24px; background: transparent;")
        icon_lbl.setFixedWidth(32)

        info = QVBoxLayout()
        info.setSpacing(2)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        detail = QLabel(f"{cat}  •  {days} days")
        detail.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        info.addWidget(name_lbl)
        info.addWidget(detail)

        check = QLabel("")
        check.setFixedSize(22, 22)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check.setStyleSheet(f"""
            font-size: 14px; background: rgba(255,255,255,0.05);
            border-radius: 11px; border: 1px solid rgba(255,255,255,0.15);
        """)

        lay.addWidget(icon_lbl)
        lay.addLayout(info, 1)
        lay.addWidget(check)

        frame.mousePressEvent = lambda e, i=idx, f=frame, c=check: self._toggle(i, f, c)
        return frame

    def _toggle(self, idx, frame, check):
        if idx in self.selected:
            self.selected.discard(idx)
            frame.setStyleSheet(CARD_CHECK_STYLE(False))
            check.setText("")
            check.setStyleSheet(f"""
                font-size: 14px; background: rgba(255,255,255,0.05);
                border-radius: 11px; border: 1px solid rgba(255,255,255,0.15);
            """)
        else:
            self.selected.add(idx)
            frame.setStyleSheet(CARD_CHECK_STYLE(True))
            check.setText("✓")
            check.setStyleSheet(f"""
                font-size: 14px; color: white;
                background: {ACCENT}; border-radius: 11px; border: none;
            """)

    def get_selected_goals(self):
        return [SUGGESTED_GOALS[i] for i in sorted(self.selected)]


# ─── صفحه ۴: آماده‌ای! ──────────────────────────────────────────────────────
class ReadyPage(QWidget):
    def __init__(self, name="Alex", parent=None):
        super().__init__(parent)
        self.name = name
        self.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(20)
        lay.setContentsMargins(60, 40, 60, 40)

        icon = QLabel("🚀")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 60px; background: transparent;")
        lay.addWidget(icon)

        self.title = QLabel(f"آماده‌ای، {name}!")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(self.title)

        sub = QLabel(
            "عادت‌ها و اهدافت ذخیره شدن.\n"
            "هر روز یه قدم کوچیک — نتایج بزرگ می‌سازه!"
        )
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(sub)

    def update_name(self, name):
        self.title.setText(f"آماده‌ای، {name}!")


# ─── Onboarding Dialog اصلی ──────────────────────────────────────────────────
class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart Life — Setup")
        self.setFixedSize(580, 520)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"""
            QDialog {{
                background: {BG_MAIN};
                border: 1px solid rgba(124,92,191,0.3);
                border-radius: 20px;
            }}
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ─ Stack ─
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        self.page_welcome = WelcomePage()
        self.page_habits  = HabitsPage()
        self.page_goals   = GoalsPage()
        self.page_ready   = ReadyPage()

        self.stack.addWidget(self.page_welcome)   # 0
        self.stack.addWidget(self.page_habits)    # 1
        self.stack.addWidget(self.page_goals)     # 2
        self.stack.addWidget(self.page_ready)     # 3

        main.addWidget(self.stack, 1)

        # ─ Progress dots ─
        dots_w = QWidget()
        dots_w.setStyleSheet("background: transparent;")
        dots_lay = QHBoxLayout(dots_w)
        dots_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dots_lay.setSpacing(8)
        self.dots = []
        for i in range(4):
            dot = QLabel("●")
            dot.setStyleSheet(f"font-size: 10px; color: {TEXT_MUTED}; background: transparent;")
            dots_lay.addWidget(dot)
            self.dots.append(dot)
        main.addWidget(dots_w)

        # ─ دکمه‌های پایین ─
        btn_w = QWidget()
        btn_w.setStyleSheet("background: transparent;")
        btn_lay = QHBoxLayout(btn_w)
        btn_lay.setContentsMargins(40, 10, 40, 24)
        btn_lay.setSpacing(12)

        self.back_btn = QPushButton("← Back")
        self.back_btn.setStyleSheet(GHOST_BTN)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._go_back)
        self.back_btn.hide()

        self.next_btn = QPushButton("شروع کنیم →")
        self.next_btn.setStyleSheet(BTN_STYLE(ACCENT, ACCENT2))
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self._go_next)

        btn_lay.addWidget(self.back_btn)
        btn_lay.addStretch()
        btn_lay.addWidget(self.next_btn)
        main.addWidget(btn_w)

        self._current = 0
        self._update_dots()

    def _go_next(self):
        if self._current == 3:
            self._finish()
            return

        if self._current == 1 and not self.page_habits.get_selected_habits():
            QMessageBox.information(
                self,
                "یک عادت انتخاب کن",
                "حداقل یک عادت انتخاب کن تا شروع کنی.",
            )
            return

        if self._current == 2:
            name = self.page_welcome.get_name()
            self.page_ready.update_name(name)

        self._current += 1
        self.stack.setCurrentIndex(self._current)
        self._update_ui()

    def _go_back(self):
        if self._current > 0:
            self._current -= 1
            self.stack.setCurrentIndex(self._current)
            self._update_ui()

    def _update_ui(self):
        self._update_dots()

        # دکمه Back
        self.back_btn.setVisible(self._current > 0)

        # متن دکمه Next
        labels = ["شروع کنیم →", "بعدی →", "بعدی →", "بزن بریم! 🚀"]
        self.next_btn.setText(labels[self._current])

    def _update_dots(self):
        for i, dot in enumerate(self.dots):
            if i == self._current:
                dot.setStyleSheet(f"font-size: 12px; color: {ACCENT2}; background: transparent;")
            else:
                dot.setStyleSheet(f"font-size: 10px; color: {TEXT_MUTED}; background: transparent;")

    def _finish(self):
        """ذخیره داده‌ها و بستن دیالوگ"""
        from datetime import date, timedelta

        name = self.page_welcome.get_name()
        settings_repo.set_user_name(name)

        for icon, name, cat, freq_type, freq_count in self.page_habits.get_selected_habits():
            habit_repo.add_habit(name, icon, cat, freq_type, freq_count)

        today = date.today()
        for icon, name, cat, days in self.page_goals.get_selected_goals():
            deadline = (today + timedelta(days=days)).isoformat()
            goal_repo.add_goal(name, f"Work towards: {name}", icon, cat, deadline)

        settings_repo.mark_onboarding_completed()
        self.accept()


# ─── تابع کمکی: آیا onboarding لازمه؟ ──────────────────────────────────────
def should_show_onboarding() -> bool:
    """اولین اجرا یا دیتابیس کاملاً خالی — onboarding نشون بده."""
    if settings_repo.is_onboarding_completed():
        return False

    habits = habit_repo.get_all_habits()
    goals = goal_repo.get_all_goals()
    if habits or goals:
        settings_repo.mark_onboarding_completed()
        return False

    return True