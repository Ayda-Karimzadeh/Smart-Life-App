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
from datetime import date, timedelta

from core.language_manager import tr

# ─── زبان‌های پیشنهادی ────────────────────────────────────────────────────────
SUGGESTED_LANGUAGES = [
    ("🇺🇸", "English", "English", "en"),
    ("🇮🇷", "فارسی", "Persian", "fa"),
]

# ─── داده‌های پیشنهادی ────────────────────────────────────────────────────────
SUGGESTED_HABITS = [

    {
        "icon": "🧘",
        "name": "habit_meditation",
        "category": "cat_mindfulness",
        "frequency": "daily",
        "count": 7
    },

    {
        "icon": "💪",
        "name": "habit_exercise",
        "category": "cat_fitness",
        "frequency": "weekly",
        "count": 3
    },

    {
        "icon": "📚",
        "name": "habit_reading",
        "category": "cat_personal_growth",
        "frequency": "daily",
        "count": 7
    },

    {
        "icon": "💧",
        "name": "habit_water",
        "category": "cat_health",
        "frequency": "daily",
        "count": 7
    },

    {
        "icon": "🌙",
        "name": "habit_sleep",
        "category": "cat_health",
        "frequency": "daily",
        "count": 7
    },

    {
        "icon": "🎸",
        "name": "habit_skill",
        "category": "cat_skills",
        "frequency": "weekly",
        "count": 3
    },

    {
        "icon": "📓",
        "name": "habit_journal",
        "category": "cat_mindfulness",
        "frequency": "daily",
        "count": 7
    },

    {
        "icon": "🏃",
        "name": "habit_walk",
        "category": "cat_fitness",
        "frequency": "daily",
        "count": 7
    }

]

SUGGESTED_GOALS = [

    {
        "icon": "🎯",
        "name": "goal_learn_something",
        "category": "cat_learning",
        "days": 90,
        "milestones": [
            ("ms_choose_topic", 3),
            ("ms_beginner_lessons", 21),
            ("ms_practice_consistently", 45),
            ("ms_build_small_project", 75),
            ("ms_master_basics", 90),
        ],
    },

    {
        "icon": "💪",
        "name": "goal_get_fit",
        "category": "cat_fitness",
        "days": 180,
        "milestones": [
            ("ms_create_workout_plan", 7),
            ("ms_complete_first_month", 30),
            ("ms_improve_endurance", 60),
            ("ms_reach_first_fitness_goal", 120),
            ("ms_keep_consistency", 180),
        ],
    },

    {
        "icon": "💰",
        "name": "goal_save_money",
        "category": "cat_finance",
        "days": 365,
        "milestones": [
            ("ms_set_saving_target", 7),
            ("ms_save_first_amount", 30),
            ("ms_save_25_percent", 120),
            ("ms_save_50_percent", 240),
            ("ms_reach_saving_goal", 365),
        ],
    },

    {
        "icon": "📖",
        "name": "goal_read_books",
        "category": "cat_personal_growth",
        "days": 365,
        "milestones": [
            ("ms_finish_first_book", 30),
            ("ms_finish_three_books", 90),
            ("ms_finish_six_books", 180),
            ("ms_finish_nine_books", 270),
            ("ms_finish_twelve_books", 365),
        ],
    },

    {
        "icon": "🚀",
        "name": "goal_side_project",
        "category": "cat_career",
        "days": 180,
        "milestones": [
            ("ms_choose_project_idea", 7),
            ("ms_plan_project", 21),
            ("ms_build_mvp", 60),
            ("ms_launch_first_version", 120),
            ("ms_improve_from_feedback", 180),
        ],
    },

    {
        "icon": "🌍",
        "name": "goal_new_language",
        "category": "cat_learning",
        "days": 365,
        "milestones": [
            ("ms_learn_alphabet", 14),
            ("ms_learn_500_words", 90),
            ("ms_first_conversation", 180),
            ("ms_reach_a2", 270),
            ("ms_reach_b1", 365),
        ],
    },

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
# صفحه 0: انتخاب زبان
class LanguagePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background: transparent;")

        self.selected_language = "en"
        self.selected_card = None
        self.selected_check = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        # Title
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            f"""
            font-size:22px;
            font-weight:bold;
            color:{TEXT_PRIMARY};
            background:transparent;
            """
        )

        # Subtitle
        self.subtitle = QLabel()
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(
            f"""
            font-size:13px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        layout.addSpacing(10)

        self.cards = []

        for icon, name, desc, code in SUGGESTED_LANGUAGES:
            card = self._create_language_card(
                icon,
                name,
                desc,
                code
            )

            layout.addWidget(card)
            self.cards.append(card)

        layout.addStretch()

        self.retranslate_ui()


    def _create_language_card(
        self,
        icon,
        name,
        desc,
        code
    ):

        frame = QFrame()

        selected = code == self.selected_language

        frame.setStyleSheet(
            CARD_CHECK_STYLE(selected)
        )

        frame.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        frame.setFixedHeight(78)

        h = QHBoxLayout(frame)
        h.setContentsMargins(16, 12, 16, 12)
        h.setSpacing(12)


        icon_label = QLabel(icon)
        icon_label.setFixedWidth(36)
        icon_label.setStyleSheet(
            """
            font-size:28px;
            background:transparent;
            """
        )


        info = QVBoxLayout()
        info.setSpacing(3)


        title_label = QLabel(name)
        title_label.setStyleSheet(
            f"""
            font-size:14px;
            font-weight:600;
            color:{TEXT_PRIMARY};
            background:transparent;
            """
        )


        subtitle_label = QLabel(desc)
        subtitle_label.setStyleSheet(
            f"""
            font-size:11px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )


        info.addWidget(title_label)
        info.addWidget(subtitle_label)


        check = QLabel()

        check.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        check.setFixedSize(22, 22)


        if selected:
            check.setText("✓")
            check.setStyleSheet(
                f"""
                color:white;
                background:{ACCENT};
                border-radius:11px;
                """
            )

            self.selected_card = frame
            self.selected_check = check

        else:
            self._set_unselected_check(check)


        h.addWidget(icon_label)
        h.addLayout(info, 1)
        h.addWidget(check)


        frame.mousePressEvent = (
            lambda e,
            c=code,
            f=frame,
            ch=check:
            self.select_language(c, f, ch)
        )


        return frame


    def _set_unselected_check(self, check):

        check.setText("")

        check.setStyleSheet(
            """
            background:rgba(255,255,255,0.05);
            border-radius:11px;
            border:1px solid rgba(255,255,255,0.15);
            """
        )


    def select_language(
        self,
        code,
        frame,
        check
    ):

        if self.selected_card:
            self.selected_card.setStyleSheet(
                CARD_CHECK_STYLE(False)
            )


        if self.selected_check:
            self._set_unselected_check(
                self.selected_check
            )


        self.selected_language = code

        self.selected_card = frame
        self.selected_check = check


        frame.setStyleSheet(
            CARD_CHECK_STYLE(True)
        )


        check.setText("✓")

        check.setStyleSheet(
            f"""
            color:white;
            background:{ACCENT};
            border-radius:11px;
            """
        )


    def retranslate_ui(self):

        self.title.setText(
            f"🌍 {tr('choose_language')}"
        )

        self.subtitle.setText(
            tr('choose_language_sub')
        )


    def get_language(self):

        return self.selected_language

# ─── صفحه 1: خوش‌آمدگویی ────────────────────────────────────────────────────
class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background: transparent;")

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(20)
        lay.setContentsMargins(60, 40, 60, 40)

        # Icon
        self.icon = QLabel("✦")
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon.setStyleSheet(
            f"""
            font-size:56px;
            color:{ACCENT2};
            background:transparent;
            """
        )
        lay.addWidget(self.icon)

        # Title
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            f"""
            font-size:28px;
            font-weight:bold;
            color:{TEXT_PRIMARY};
            background:transparent;
            line-height:1.4;
            """
        )
        lay.addWidget(self.title)

        # Description
        self.sub = QLabel()
        self.sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub.setWordWrap(True)
        self.sub.setStyleSheet(
            f"""
            font-size:14px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )
        lay.addWidget(self.sub)

        lay.addSpacing(10)

        # Name label
        self.name_lbl = QLabel()
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setStyleSheet(
            f"""
            font-size:13px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )
        lay.addWidget(self.name_lbl)

        # Name edit
        self.name_edit = QLineEdit()
        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_edit.setMaximumWidth(300)
        self.name_edit.setStyleSheet(
            f"""
            QLineEdit {{
                background:{BG_CARD2};
                color:{TEXT_PRIMARY};
                border:2px solid rgba(255,255,255,0.10);
                border-radius:10px;
                padding:10px 16px;
                font-size:15px;
            }}

            QLineEdit:focus {{
                border:2px solid {ACCENT};
            }}
            """
        )

        lay.addWidget(
            self.name_edit,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        # Load translations
        self.retranslate_ui()

    def retranslate_ui(self):
        """Update all texts when language changes."""

        self.title.setText(tr("welcome"))
        self.sub.setText(tr("onboarding_desc"))
        self.name_lbl.setText(tr("your_name"))
        self.name_edit.setPlaceholderText(
            tr("name_placeholder")
        )

    def get_name(self):
        name = self.name_edit.text().strip()
        return name if name else tr("default_name")


# ─── صفحه ۲: انتخاب عادت‌ها ─────────────────────────────────────────────────
class HabitsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(
            "background:transparent;"
        )

        self.selected = set()
        self.cards = []

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            40,30,40,30
        )

        self.main_layout.setSpacing(
            16
        )


        # Title
        self.title = QLabel()

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet(
            f"""
            font-size:20px;
            font-weight:bold;
            color:{TEXT_PRIMARY};
            background:transparent;
            """
        )


        # Subtitle
        self.subtitle = QLabel()

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle.setStyleSheet(
            f"""
            font-size:13px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )


        self.main_layout.addWidget(
            self.title
        )

        self.main_layout.addWidget(
            self.subtitle
        )


        # Scroll

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        scroll.setStyleSheet(
            """
            QScrollArea{
                border:none;
                background:transparent;
            }
            """
        )


        container = QWidget()

        container.setStyleSheet(
            "background:transparent;"
        )


        self.cards_layout = QVBoxLayout(
            container
        )

        self.cards_layout.setSpacing(
            10
        )


        self.create_cards()


        scroll.setWidget(
            container
        )


        self.main_layout.addWidget(
            scroll
        )


        self.retranslate_ui()



    def create_cards(self):

        for row in range(
            0,
            len(SUGGESTED_HABITS),
            2
        ):

            row_widget = QWidget()

            row_layout = QHBoxLayout(
                row_widget
            )

            row_layout.setSpacing(
                10
            )


            for col in range(2):

                index = row + col


                if index >= len(SUGGESTED_HABITS):

                    row_layout.addStretch()
                    break


                card = self.create_card(
                    index,
                    SUGGESTED_HABITS[index]
                )


                row_layout.addWidget(
                    card
                )

                self.cards.append(
                    card
                )


            self.cards_layout.addWidget(
                row_widget
            )



    def create_card(
        self,
        index,
        habit
    ):

        frame = QFrame()

        frame.setFixedHeight(
            70
        )

        frame.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        frame.setStyleSheet(
            CARD_CHECK_STYLE(False)
        )


        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,10,14,10
        )


        icon = QLabel(
            habit["icon"]
        )

        icon.setStyleSheet(
            """
            font-size:24px;
            background:transparent;
            """
        )


        info = QVBoxLayout()


        name = QLabel(
            tr(habit["name"])
        )

        name.setStyleSheet(
            f"""
            color:{TEXT_PRIMARY};
            font-size:13px;
            font-weight:600;
            background:transparent;
            """
        )


        category = QLabel(
            tr(habit["category"])
        )

        category.setStyleSheet(
            f"""
            color:{TEXT_MUTED};
            font-size:11px;
            background:transparent;
            """
        )


        info.addWidget(
            name
        )

        info.addWidget(
            category
        )


        check = QLabel()

        check.setFixedSize(
            22,22
        )

        check.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.set_unselected(
            check
        )


        layout.addWidget(
            icon
        )

        layout.addLayout(
            info,
            1
        )

        layout.addWidget(
            check
        )


        frame.mousePressEvent = (
            lambda e,
            i=index,
            f=frame,
            c=check:
            self.toggle_card(i,f,c)
        )

        frame.name_label = name
        frame.category_label = category
        frame.habit = habit

        return frame



    def toggle_card(
        self,
        index,
        frame,
        check
    ):

        if index in self.selected:

            self.selected.remove(
                index
            )

            frame.setStyleSheet(
                CARD_CHECK_STYLE(False)
            )

            self.set_unselected(
                check
            )


        else:

            self.selected.add(
                index
            )

            frame.setStyleSheet(
                CARD_CHECK_STYLE(True)
            )

            check.setText(
                "✓"
            )

            check.setStyleSheet(
                f"""
                color:white;
                background:{ACCENT};
                border-radius:11px;
                """
            )



    def set_unselected(
        self,
        check
    ):

        check.setText("")

        check.setStyleSheet(
            """
            background:rgba(255,255,255,0.05);
            border-radius:11px;
            border:1px solid rgba(255,255,255,0.15);
            """
        )



    def get_selected_habits(self):

        return [
            SUGGESTED_HABITS[i]
            for i in sorted(self.selected)
        ]



    def retranslate_ui(self):

        self.title.setText(
            tr("select_habits")
        )

        self.subtitle.setText(
            tr("select_habits_sub")
        )

        for card in self.cards:

            card.name_label.setText(
                tr(card.habit["name"])
            )

            card.category_label.setText(
                tr(card.habit["category"])
            )

# ─── صفحه ۳: انتخاب هدف ─────────────────────────────────────────────────────
class GoalsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.selected = set()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(40, 30, 40, 30)
        lay.setSpacing(16)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(self.title)

        self.sub = QLabel()
        self.sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(self.sub)

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
                goal = SUGGESTED_GOALS[idx]
                card = self._make_goal_card(idx, goal)
                row_lay.addWidget(card)

            grid_lay.addWidget(row_w)

        lay.addWidget(grid_widget)

        self.retranslate_ui()

        lay.addStretch()

    def retranslate_ui(self):
        self.title.setText(tr("select_goals"))
        self.sub.setText(tr("select_goals_sub"))

    def _make_goal_card(self, idx, goal):
        frame = QFrame()
        frame.setStyleSheet(CARD_CHECK_STYLE(False))
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        frame.setFixedHeight(70)

        lay = QHBoxLayout(frame)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        icon_lbl = QLabel(goal["icon"])
        icon_lbl.setStyleSheet("font-size: 24px; background: transparent;")
        icon_lbl.setFixedWidth(32)

        info = QVBoxLayout()
        info.setSpacing(2)
        name_lbl = QLabel(tr(goal["name"]))
        name_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        detail = QLabel(
            f"{tr(goal['category'])} • {goal['days']} {tr('days')}"
        )
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

        frame.name_label = name_lbl
        frame.detail_label = detail
        frame.goal = goal

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
        icon.setStyleSheet("font-size:60px; background:transparent;")
        lay.addWidget(icon)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            f"""
            font-size:28px;
            font-weight:bold;
            color:{TEXT_PRIMARY};
            background:transparent;
            """
        )
        lay.addWidget(self.title)

        self.sub = QLabel()
        self.sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub.setStyleSheet(
            f"""
            font-size:14px;
            color:{TEXT_MUTED};
            background:transparent;
            """
        )
        lay.addWidget(self.sub)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.title.setText(
            tr("ready_title").format(name=self.name)
        )
        self.sub.setText(
            tr("ready_desc")
        )

    def update_name(self, name):
        self.name = name
        self.retranslate_ui()

# ─── Onboarding Dialog اصلی ──────────────────────────────────────────────────
class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Smart Life — Setup")
        self.setFixedSize(580, 520)

        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint
        )

        self.setStyleSheet(
            f"""
            QDialog {{
                background:{BG_MAIN};
                border:1px solid rgba(124,92,191,0.3);
                border-radius:20px;
            }}
            """
        )


        main = QVBoxLayout(self)
        main.setContentsMargins(0,0,0,0)
        main.setSpacing(0)


        # Pages
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(
            "background:transparent;"
        )


        self.page_language = LanguagePage()
        self.page_welcome = WelcomePage()
        self.page_habits = HabitsPage()
        self.page_goals = GoalsPage()
        self.page_ready = ReadyPage()


        pages = [
            self.page_language,
            self.page_welcome,
            self.page_habits,
            self.page_goals,
            self.page_ready
        ]


        for page in pages:
            self.stack.addWidget(page)


        main.addWidget(self.stack,1)



        # Progress dots
        dots_w = QWidget()
        dots_w.setStyleSheet(
            "background:transparent;"
        )

        dots_lay = QHBoxLayout(dots_w)
        dots_lay.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        dots_lay.setSpacing(8)


        self.dots = []

        for _ in range(5):

            dot = QLabel("●")

            dot.setStyleSheet(
                f"""
                font-size:10px;
                color:{TEXT_MUTED};
                background:transparent;
                """
            )

            dots_lay.addWidget(dot)
            self.dots.append(dot)


        main.addWidget(dots_w)



        # Buttons
        btn_w = QWidget()
        btn_w.setStyleSheet(
            "background:transparent;"
        )


        btn_lay = QHBoxLayout(btn_w)

        btn_lay.setContentsMargins(
            40,10,40,24
        )

        btn_lay.setSpacing(12)


        self.back_btn = QPushButton()

        self.back_btn.setStyleSheet(
            GHOST_BTN
        )

        self.back_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.back_btn.clicked.connect(
            self._go_back
        )

        self.back_btn.hide()



        self.next_btn = QPushButton()

        self.next_btn.setStyleSheet(
            BTN_STYLE(ACCENT,ACCENT2)
        )

        self.next_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.next_btn.clicked.connect(
            self._go_next
        )


        btn_lay.addWidget(
            self.back_btn
        )

        btn_lay.addStretch()

        btn_lay.addWidget(
            self.next_btn
        )


        main.addWidget(btn_w)


        self._current = 0

        self.retranslate_ui()

        self._update_dots()



    def _go_next(self):

        # انتخاب زبان
        if self._current == 0:

            from core.language_manager import get_language_manager

            language = self.page_language.get_language()

            get_language_manager().set_language(language)

            self.retranslate_ui()



        # چک کردن عادت
        if self._current == 2:

            if not self.page_habits.get_selected_habits():

                QMessageBox.information(
                    self,
                    tr("select_habit_error"),
                    tr("select_habit_error_desc")
                )

                return



        # قبل از Ready
        if self._current == 3:

            name = (
                self.page_welcome
                .get_name()
            )

            self.page_ready.update_name(
                name
            )


        if self._current == 4:

            self._finish()
            return



        self._current += 1

        self.stack.setCurrentIndex(
            self._current
        )

        self._update_ui()



    def _go_back(self):

        if self._current > 0:

            self._current -= 1

            self.stack.setCurrentIndex(
                self._current
            )

            self._update_ui()



    def retranslate_ui(self):
        self.page_language.retranslate_ui()
        self.page_welcome.retranslate_ui()
        self.page_habits.retranslate_ui()
        self.page_goals.retranslate_ui()
        self.page_ready.retranslate_ui()

        self.back_btn.setText(
        tr("back")
        )

        self._update_ui()


    def _update_ui(self):

        self._update_dots()

        # Back button
        self.back_btn.setVisible(
            self._current > 0
        )

        # Next button text
        labels = [
            "continue",    # Language
            "lets_start",  # Welcome
            "next",        # Habits
            "next",        # Goals
            "lets_go"      # Ready
        ]

        self.next_btn.setText(
            tr(labels[self._current])
        )
  


    def _update_dots(self):

        for i,dot in enumerate(self.dots):

            if i == self._current:

                dot.setStyleSheet(
                    f"""
                    font-size:12px;
                    color:{ACCENT2};
                    background:transparent;
                    """
                )

            else:

                dot.setStyleSheet(
                    f"""
                    font-size:10px;
                    color:{TEXT_MUTED};
                    background:transparent;
                    """
                )



    def _finish(self):

        name = self.page_welcome.get_name()

        settings_repo.set_user_name(
            name
        )


        for habit in self.page_habits.get_selected_habits():

            habit_repo.add_habit(
                habit["name"],
                habit["icon"],
                habit["category"],
                habit["frequency"],
                habit["count"]
            )


        today = date.today()


        for goal in self.page_goals.get_selected_goals():

            deadline = (
                today +
                timedelta(days=goal["days"])
            ).isoformat()


            goal_id = goal_repo.add_goal(
                name=goal["name"],
                description="",
                icon=goal["icon"],
                category=goal["category"],
                deadline=deadline,
            )


            for milestone_name, days in goal["milestones"]:

                goal_repo.add_milestone(
                    goal_id,
                    milestone_name
                )


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