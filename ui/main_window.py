from datetime import date

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget
)
from PyQt6.QtCore import Qt

from assets.style import (
    GLOBAL_STYLE, BG_MAIN, BG_CARD,
    TEXT_PRIMARY, TEXT_MUTED, ORANGE, ACCENT2,
    placeholder_page
)
from ui.sidebar import Sidebar
from ui.dashboard_page import DashboardPage
from ui.habits_page    import HabitsPage
from ui.goals_page     import GoalsPage
from ui.tasks_page     import TasksPage
from ui.timer_page     import TimerPage
from ui.analytics_page import AnalyticsPage
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
)


# ─── Header ───────────────────────────────────────────────────────────────────
class Header(QWidget):
    PAGE_NAMES = [
        "Dashboard", "Habits", "Goals",
        "Tasks", "Time Tracking", "Analytics"
    ]

    def __init__(self):
        super().__init__()
        self.setFixedHeight(64)
        self.setStyleSheet(
            f"background: {BG_MAIN}; "
            f"border-bottom: 1px solid rgba(255,255,255,0.05);"
        )

        lay = QHBoxLayout(self)
        lay.setContentsMargins(28, 0, 28, 0)

        self.title = QLabel("Dashboard")
        self.title.setStyleSheet(
            f"font-size: 20px; font-weight: bold; "
            f"color: {TEXT_PRIMARY}; background: transparent;"
        )

        today = date.today().strftime("%A, %B %d, %Y")
        self.date_lbl = QLabel(today)
        self.date_lbl.setStyleSheet(
            f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;"
        )

        left = QVBoxLayout()
        left.setSpacing(2)
        left.addWidget(self.title)
        left.addWidget(self.date_lbl)

        # Streak و Score از دیتابیس
        habits = habit_repo.get_all_habits()
        max_streak = max(
            (habit_repo.get_current_streak(h.id) for h in habits), default=0
        ) if habits else 0

        self.streak_lbl = QLabel(f"🔥  Streak  {max_streak} days")
        self.streak_lbl.setStyleSheet(f"""
            background: {BG_CARD};
            color: {ORANGE};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
        """)

        # Productivity score
        from core.analytics import productivity_score
        score = productivity_score()
        self.score_lbl = QLabel(f"🏆  Score  {score}%")
        self.score_lbl.setStyleSheet(f"""
            background: {BG_CARD};
            color: {ACCENT2};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
        """)

        lay.addLayout(left)
        lay.addStretch()
        lay.addWidget(self.streak_lbl)
        lay.addSpacing(10)
        lay.addWidget(self.score_lbl)

    def set_page(self, idx):
        self.title.setText(self.PAGE_NAMES[idx])

    def refresh_stats(self):
        """آپدیت streak و score در هدر"""
        habits = habit_repo.get_all_habits()
        max_streak = max(
            (habit_repo.get_current_streak(h.id) for h in habits), default=0
        ) if habits else 0
        self.streak_lbl.setText(f"🔥  Streak  {max_streak} days")

        from core.analytics import productivity_score
        score = productivity_score()
        self.score_lbl.setText(f"🏆  Score  {score}%")


# ─── MainWindow ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Life Dashboard")
        self.resize(1280, 780)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(GLOBAL_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        self.header = Header()
        root.addWidget(self.header)

        # Body
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # Stack
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        # ساخت همه صفحه‌ها
        self.dashboard_page  = DashboardPage()
        self.habits_page     = HabitsPage()
        self.goals_page      = GoalsPage()
        self.tasks_page      = TasksPage()
        self.timer_page      = TimerPage()
        self.analytics_page  = AnalyticsPage()

        pages = [
            self.dashboard_page,
            self.habits_page,
            self.goals_page,
            self.tasks_page,
            self.timer_page,
            self.analytics_page,
        ]
        for p in pages:
            self.stack.addWidget(p)

        # Sidebar
        self.sidebar = Sidebar(self._switch_page)

        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)
        root.addLayout(body, 1)

    def _switch_page(self, idx):
        """سوئیچ بین صفحه‌ها + refresh صفحه مقصد"""
        self.stack.setCurrentIndex(idx)
        self.header.set_page(idx)
        self.header.refresh_stats()

        # refresh صفحه‌ای که بهش رفتیم
        page = self.stack.currentWidget()
        if hasattr(page, "refresh"):
            page.refresh()