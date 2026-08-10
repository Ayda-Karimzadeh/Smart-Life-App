from datetime import date

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
)

from ui.dialogs import SettingsDialog

from core.language_manager import (
    tr,
    get_language_manager,
)

from assets.style import (
    GLOBAL_STYLE,
    BG_MAIN,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_MUTED,
    ORANGE,
    ACCENT2,
)

from ui.sidebar import Sidebar
from ui.dashboard_page import DashboardPage
from ui.habits_page import HabitsPage
from ui.goals_page import GoalsPage
from ui.tasks_page import TasksPage
from ui.timer_page import TimerPage
from ui.analytics_page import AnalyticsPage

from database.repository import habit_repo


# ─── Header ───────────────────────────────────────────────────────────────────

class Header(QWidget):

    PAGE_KEYS = [
        "dashboard",
        "habits",
        "goals",
        "tasks",
        "time_tracking",
        "analytics",
    ]

    def __init__(self):
        super().__init__()

        self.setFixedHeight(64)

        self.setStyleSheet(
            f"background: {BG_MAIN}; "
            f"border-bottom: 1px solid rgba(255,255,255,0.05);"
        )

        # صفحه فعلی
        self.current_page = 0

        # ─── Layout ───────────────────────────────────────────────────────

        lay = QHBoxLayout(self)
        lay.setContentsMargins(28, 0, 28, 0)

        # ─── Title ────────────────────────────────────────────────────────

        self.title = QLabel(
            tr(self.PAGE_KEYS[self.current_page])
        )

        self.title.setStyleSheet(
            f"font-size: 20px; "
            f"font-weight: bold; "
            f"color: {TEXT_PRIMARY}; "
            f"background: transparent;"
        )

        # ─── Date ─────────────────────────────────────────────────────────

        today = date.today().strftime("%A, %B %d, %Y")

        self.date_lbl = QLabel(today)

        self.date_lbl.setStyleSheet(
            f"font-size: 12px; "
            f"color: {TEXT_MUTED}; "
            f"background: transparent;"
        )

        left = QVBoxLayout()
        left.setSpacing(2)

        left.addWidget(self.title)
        left.addWidget(self.date_lbl)

        # ─── Streak ───────────────────────────────────────────────────────

        habits = habit_repo.get_all_habits()

        max_streak = max(
            (
                habit_repo.get_current_streak(h.id)
                for h in habits
            ),
            default=0,
        ) if habits else 0

        self.streak_value = max_streak

        self.streak_lbl = QLabel()

        self.streak_lbl.setStyleSheet(
            f"""
            background: {BG_CARD};
            color: {ORANGE};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
            """
        )

        # ─── Productivity Score ──────────────────────────────────────────

        from core.analytics import productivity_score

        self.score_value = productivity_score()

        self.score_lbl = QLabel()

        self.score_lbl.setStyleSheet(
            f"""
            background: {BG_CARD};
            color: {ACCENT2};
            border-radius: 10px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
            """
        )

        # مقداردهی اولیه متن‌ها
        self.update_stats_labels()

        # ─── Header Layout ────────────────────────────────────────────────

        lay.addLayout(left)
        lay.addStretch()

        lay.addWidget(self.streak_lbl)
        lay.addSpacing(10)
        lay.addWidget(self.score_lbl)

    # ─────────────────────────────────────────────────────────────────────
    # Update translated texts
    # ─────────────────────────────────────────────────────────────────────

    def update_translations(self):
        """
        به‌روزرسانی متن‌های Header بعد از تغییر زبان.
        """

        # عنوان صفحه فعلی
        self.title.setText(
            tr(self.PAGE_KEYS[self.current_page])
        )

        # Streak / Score
        self.update_stats_labels()

    # ─────────────────────────────────────────────────────────────────────
    # Update stats labels
    # ─────────────────────────────────────────────────────────────────────

    def update_stats_labels(self):
        """
        فقط متن Streak و Score را با زبان فعلی آپدیت می‌کند.
        """

        self.streak_lbl.setText(
            f"🔥  {tr('streak')}  "
            f"{self.streak_value} "
            f"{tr('days')}"
        )

        self.score_lbl.setText(
            f"🏆  {tr('score')}  "
            f"{self.score_value}%"
        )

    # ─────────────────────────────────────────────────────────────────────
    # Change current page
    # ─────────────────────────────────────────────────────────────────────

    def set_page(self, idx):
        """
        تغییر عنوان Header بر اساس صفحه انتخاب‌شده.
        """

        if 0 <= idx < len(self.PAGE_KEYS):
            self.current_page = idx

            self.title.setText(
                tr(self.PAGE_KEYS[idx])
            )

    # ─────────────────────────────────────────────────────────────────────
    # Refresh statistics
    # ─────────────────────────────────────────────────────────────────────

    def refresh_stats(self):
        """
        دریافت دوباره Streak و Productivity Score
        و نمایش آن‌ها با زبان فعلی.
        """

        habits = habit_repo.get_all_habits()

        max_streak = max(
            (
                habit_repo.get_current_streak(h.id)
                for h in habits
            ),
            default=0,
        ) if habits else 0

        self.streak_value = max_streak

        from core.analytics import productivity_score

        self.score_value = productivity_score()

        self.update_stats_labels()


# ─── MainWindow ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ─── Window ───────────────────────────────────────────────────────

        self.setWindowTitle(
            tr("app_name")
        )

        self.resize(1280, 780)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(GLOBAL_STYLE)

        # ─── Central Widget ───────────────────────────────────────────────

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ─── Header ───────────────────────────────────────────────────────

        self.header = Header()

        root.addWidget(self.header)

        # ─── Body ─────────────────────────────────────────────────────────

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # ─── Stack ────────────────────────────────────────────────────────

        self.stack = QStackedWidget()

        self.stack.setStyleSheet(
            "background: transparent;"
        )

        # ─── Pages ────────────────────────────────────────────────────────

        self.dashboard_page = DashboardPage()
        self.habits_page = HabitsPage()
        self.goals_page = GoalsPage()
        self.tasks_page = TasksPage()
        self.timer_page = TimerPage()
        self.analytics_page = AnalyticsPage()

        self._add_pages()

        # ─── Sidebar ──────────────────────────────────────────────────────

        self.sidebar = Sidebar(
            self._switch_page,
            self.open_settings
        )

        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)

        root.addLayout(body, 1)

        # ─── Language Manager ─────────────────────────────────────────────

        self.language_manager = get_language_manager()

        self.language_manager.language_changed.connect(
            self.language_changed
        )

    # ─────────────────────────────────────────────────────────────────────
    # Add pages to stack
    # ─────────────────────────────────────────────────────────────────────

    def _add_pages(self):

        pages = [
            self.dashboard_page,
            self.habits_page,
            self.goals_page,
            self.tasks_page,
            self.timer_page,
            self.analytics_page,
        ]

        for page in pages:
            self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────
    # Language changed
    # ─────────────────────────────────────────────────────────────────────

    def language_changed(self, lang):

        print("Language changed:", lang)

        # عنوان پنجره
        self.setWindowTitle(
            tr("app_name")
        )

        # Sidebar
        self.sidebar.update_translations()

        # Header
        self.header.update_translations()

        # ساخت دوباره صفحات با زبان جدید
        self.rebuild_pages()

    # ─────────────────────────────────────────────────────────────────────
    # Settings
    # ─────────────────────────────────────────────────────────────────────

    def open_settings(self):

        dlg = SettingsDialog(self)
        dlg.exec()

    # ─────────────────────────────────────────────────────────────────────
    # Rebuild pages after language change
    # ─────────────────────────────────────────────────────────────────────

    def rebuild_pages(self):

        # صفحه فعلی را قبل از rebuild ذخیره می‌کنیم
        current_index = self.stack.currentIndex()

        # جلوگیری از خارج شدن index
        if current_index < 0:
            current_index = 0

        # صفحات قبلی را از Stack حذف می‌کنیم
        old_pages = [
            self.dashboard_page,
            self.habits_page,
            self.goals_page,
            self.tasks_page,
            self.timer_page,
            self.analytics_page,
        ]

        for page in old_pages:
            self.stack.removeWidget(page)

            # حذف واقعی widget قدیمی
            page.deleteLater()

        # ─── ساخت دوباره صفحات ───────────────────────────────────────────

        self.dashboard_page = DashboardPage()
        self.habits_page = HabitsPage()
        self.goals_page = GoalsPage()
        self.tasks_page = TasksPage()
        self.timer_page = TimerPage()
        self.analytics_page = AnalyticsPage()

        # ─── اضافه کردن صفحات جدید ────────────────────────────────────────

        self._add_pages()

        # ─── برگرداندن صفحه قبلی ──────────────────────────────────────────

        if current_index >= self.stack.count():
            current_index = 0

        self.stack.setCurrentIndex(current_index)

        # Header را هم با صفحه فعلی هماهنگ می‌کنیم
        self.header.set_page(current_index)

        # آمار را دوباره محاسبه می‌کنیم
        self.header.refresh_stats()

    # ─────────────────────────────────────────────────────────────────────
    # Switch page
    # ─────────────────────────────────────────────────────────────────────

    def _switch_page(self, idx):
        """
        سوئیچ بین صفحه‌ها + refresh صفحه مقصد
        """

        if idx < 0 or idx >= self.stack.count():
            return

        # تغییر صفحه
        self.stack.setCurrentIndex(idx)

        # تغییر عنوان Header
        self.header.set_page(idx)

        # آپدیت Streak / Score
        self.header.refresh_stats()

        # refresh صفحه مقصد
        page = self.stack.currentWidget()

        if hasattr(page, "refresh"):
            page.refresh()

    # ─────────────────────────────────────────────────────────────────────
    # Onboarding
    # ─────────────────────────────────────────────────────────────────────

    def maybe_run_onboarding(self):
        """
        اولین اجرا: onboarding را نمایش می‌دهد.
        """

        from ui.onboarding import (
            OnboardingDialog,
            should_show_onboarding,
        )

        if not should_show_onboarding():
            return

        dlg = OnboardingDialog(self)

        if dlg.exec():
            self.refresh_all()

    # ─────────────────────────────────────────────────────────────────────
    # Refresh everything
    # ─────────────────────────────────────────────────────────────────────

    def refresh_all(self):
        """
        بعد از onboarding یا تغییرات بزرگ،
        همه صفحه‌ها را آپدیت می‌کند.
        """

        # Sidebar
        self.sidebar.update_translations()

        # Header
        self.header.update_translations()
        self.header.refresh_stats()

        # همه صفحات
        for i in range(self.stack.count()):

            page = self.stack.widget(i)

            if hasattr(page, "refresh"):
                page.refresh()