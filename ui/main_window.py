from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget
)
from PyQt6.QtCore import Qt
from assets.style import GLOBAL_STYLE, BG_MAIN, BG_CARD, TEXT_PRIMARY, TEXT_MUTED, ORANGE, ACCENT2, placeholder_page
from ui.sidebar import Sidebar
from ui.dashboard_page import DashboardPage
from ui.habits_page import HabitsPage
from ui.tasks_page import TasksPage
from datetime import date
from ui.goals_page import GoalsPage
from ui.timer_page import TimerPage
from ui.analytics_page import AnalyticsPage

class Header(QWidget):
    PAGE_NAMES = ["Dashboard", "Habits", "Goals", "Tasks", "Time Tracking", "Analytics"]

    def __init__(self):
        super().__init__()
        self.setFixedHeight(64)
        self.setStyleSheet(f"background: {BG_MAIN}; border-bottom: 1px solid rgba(255,255,255,0.05);")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(28, 0, 28, 0)

        self.title = QLabel("Dashboard")
        self.title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")

        today = date.today().strftime("%A, %B %d, %Y")
        self.date_lbl = QLabel(today)
        self.date_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")

        left = QVBoxLayout()
        left.setSpacing(2)
        left.addWidget(self.title)
        left.addWidget(self.date_lbl)

        streak = QLabel("🔥  Streak  24 days")
        streak.setStyleSheet(f"""
            background: {BG_CARD};
            color: {ORANGE};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
        """)
        score = QLabel("🏆  Score  92%")
        score.setStyleSheet(f"""
            background: {BG_CARD};
            color: {ACCENT2};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
        """)

        lay.addLayout(left)
        lay.addStretch()
        lay.addWidget(streak)
        lay.addSpacing(10)
        lay.addWidget(score)

    def set_page(self, idx):
        self.title.setText(self.PAGE_NAMES[idx])


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

        self.header = Header()
        root.addWidget(self.header)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")

        pages = [
            DashboardPage(),
            HabitsPage(),
            GoalsPage(),
            TasksPage(),
            TimerPage(),
            AnalyticsPage(),
        ]
        for p in pages:
            self.stack.addWidget(p)

        self.sidebar = Sidebar(self._switch_page)

        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)
        root.addLayout(body, 1)

    def _switch_page(self, idx):
        self.stack.setCurrentIndex(idx)
        self.header.set_page(idx)
