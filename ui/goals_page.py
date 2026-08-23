from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QFrame, QProgressBar, QGridLayout,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import date, datetime

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)
from database.repository import goal_repo
from ui.dialogs import AddGoalDialog, AddMilestoneDialog
from core.language_manager import tr


# =========================================================
# Goal Category Translation
# =========================================================

# کلیدها به‌صورت lower-case نگه داشته می‌شن تا مچ‌شدن مستقل از
# حروف بزرگ/کوچیکِ رشته‌ی ذخیره‌شده در دیتابیس باشه
# (مثلاً "Career", "career", "CAREER" همه باید یک ترجمه بگیرن).
GOAL_CATEGORY_TRANSLATION_KEYS = {
    "all": "all",
    "career": "career",
    "personal": "personal",
    "health": "health",
    "finance": "finance",
    "education": "education",
    "other": "other",
}


def translate_goal_category(category):
    """
    دسته‌بندی رو مستقل از حروف بزرگ/کوچیک و فاصله‌های اضافه ترجمه می‌کند.
    اگه کلید توی دیکشنری پیدا نشه، خودِ متن خام (بدون تغییر) برگردونده می‌شه
    تا حداقل چیزی نمایش داده بشه (به‌جای کرش یا رشته‌ی خالی).
    """
    if category is None:
        return ""

    normalized = str(category).strip().lower()
    key = GOAL_CATEGORY_TRANSLATION_KEYS.get(normalized)

    if key:
        return tr(key)

    # اگه دسته‌بندی سفارشی/ناشناخته بود، همون متن اصلی (با حروف اولیه‌اش) نشون داده بشه
    return str(category).strip()


repo = goal_repo


# =========================================================
# Goal Colors
# =========================================================

GOAL_COLORS = [
    (ACCENT2, "#1a1535"),
    (ORANGE, "#2a1a0a"),
    (BLUE, "#0a1a2a"),
    (GREEN, "#0a2a1a"),
    (ACCENT, "#1a1535"),
]


def _days_left(deadline_str):
    if not deadline_str:
        return None

    try:
        d = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        return (d - date.today()).days
    except ValueError:
        return None


# =========================================================
# Goal Card
# =========================================================

class GoalCard(QWidget):

    def __init__(self, goal, color, bg_color, on_change, parent=None):
        super().__init__(parent)

        self.goal = goal
        self.on_change = on_change

        self.setStyleSheet("background: transparent;")

        milestones = repo.get_milestones(goal.id)
        progress = repo.get_goal_progress_percent(goal.id)
        days_left = _days_left(goal.deadline)

        card = make_card(color=bg_color)
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        lay = QVBoxLayout(card)
        lay.setContentsMargins(22, 20, 22, 20)
        lay.setSpacing(12)

        # ─────────────────────────────────────────────
        # Top Row
        # ─────────────────────────────────────────────

        top = QHBoxLayout()

        icon_box = QLabel(goal.icon)
        icon_box.setFixedSize(50, 50)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet(
            "font-size: 24px;"
            "background: rgba(255,255,255,0.1);"
            "border-radius: 14px;"
        )

        info = QVBoxLayout()
        info.setSpacing(4)

        name_lbl = QLabel(tr(goal.name))
        name_lbl.setStyleSheet(
            f"font-size: 17px;"
            f"font-weight: bold;"
            f"color: {TEXT_PRIMARY};"
            f"background: transparent;"
        )

        desc_lbl = QLabel(goal.description)
        desc_lbl.setStyleSheet(
            f"font-size: 12px;"
            f"color: {TEXT_MUTED};"
            f"background: transparent;"
        )
        desc_lbl.setWordWrap(True)

        tags = QHBoxLayout()
        tags.setSpacing(8)

        # Category translation
        cat_lbl = QLabel(
            translate_goal_category(goal.category)
        )
        cat_lbl.setStyleSheet(
            f"""
            font-size: 11px;
            color: {TEXT_PRIMARY};
            background: rgba(255,255,255,0.12);
            border-radius: 6px;
            padding: 2px 10px;
            """
        )

        tags.addWidget(cat_lbl)

        if days_left is not None:

            if days_left < 0:
                days_text = (
                    f"📅 {abs(days_left)} "
                    f"{tr('days_overdue')}"
                )

            elif days_left == 0:
                days_text = f"📅 {tr('due_today')}"

            else:
                days_text = (
                    f"📅 {days_left} "
                    f"{tr('days_left')}"
                )

            days_lbl = QLabel(days_text)
            days_lbl.setStyleSheet(
                f"font-size: 11px;"
                f"color: {TEXT_MUTED};"
                f"background: transparent;"
            )

            tags.addWidget(days_lbl)

        tags.addStretch()

        info.addWidget(name_lbl)

        if goal.description:
            info.addWidget(desc_lbl)

        info.addLayout(tags)

        # ─────────────────────────────────────────────
        # Progress / Actions
        # ─────────────────────────────────────────────

        pct_col = QVBoxLayout()
        pct_col.setAlignment(
            Qt.AlignmentFlag.AlignTop |
            Qt.AlignmentFlag.AlignRight
        )

        pct_lbl = QLabel(f"{progress}%")
        pct_lbl.setStyleSheet(
            f"font-size: 28px;"
            f"font-weight: bold;"
            f"color: {color};"
            f"background: transparent;"
        )
        pct_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)

        complete_lbl = QLabel(tr("progress"))
        complete_lbl.setStyleSheet(
            f"font-size: 11px;"
            f"color: {TEXT_MUTED};"
            f"background: transparent;"
        )
        complete_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)

        pct_col.addWidget(pct_lbl)
        pct_col.addWidget(complete_lbl)

        actions = QHBoxLayout()
        actions.setSpacing(4)

        edit_btn = self._icon_button("✏️")
        edit_btn.clicked.connect(self._handle_edit)

        delete_btn = self._icon_button(
            "🗑️",
            danger=True
        )
        delete_btn.clicked.connect(self._handle_delete)

        actions.addWidget(edit_btn)
        actions.addWidget(delete_btn)

        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_col.addLayout(actions)
        right_col.addLayout(pct_col)

        top.addWidget(icon_box)
        top.addSpacing(12)
        top.addLayout(info, 1)
        top.addLayout(right_col)

        lay.addLayout(top)

        # ─────────────────────────────────────────────
        # Progress Bar
        # ─────────────────────────────────────────────

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(progress)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)

        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background: rgba(255,255,255,0.1);
                border-radius: 4px;
            }}

            QProgressBar::chunk {{
                background: {color};
                border-radius: 4px;
            }}
            """
        )

        lay.addWidget(bar)

        # ─────────────────────────────────────────────
        # Milestones
        # ─────────────────────────────────────────────

        done_count = sum(
            1 for m in milestones if m.done
        )

        ms_header = QHBoxLayout()

        ms_lbl = QLabel(tr("milestones"))
        ms_lbl.setStyleSheet(
            f"font-size: 13px;"
            f"font-weight: 600;"
            f"color: {TEXT_PRIMARY};"
            f"background: transparent;"
        )

        ms_count = QLabel(
            tr("milestones_completed").format(
                done=done_count,
                total=len(milestones)
            )
        )

        ms_count.setStyleSheet(
            f"font-size: 11px;"
            f"color: {TEXT_MUTED};"
            f"background: transparent;"
        )

        add_ms_btn = QPushButton(
            "+ " + tr("add")
        )

        add_ms_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        add_ms_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: rgba(255,255,255,0.08);
                color: {TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: 3px 12px;
                font-size: 11px;
            }}

            QPushButton:hover {{
                background: rgba(255,255,255,0.15);
            }}
            """
        )

        add_ms_btn.clicked.connect(
            self._handle_add_milestone
        )

        ms_header.addWidget(ms_lbl)
        ms_header.addStretch()
        ms_header.addWidget(ms_count)
        ms_header.addSpacing(8)
        ms_header.addWidget(add_ms_btn)

        lay.addLayout(ms_header)

        if milestones:

            grid = QGridLayout()
            grid.setSpacing(8)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)

            for i, m in enumerate(milestones):
                grid.addWidget(
                    self._milestone_widget(m),
                    i // 2,
                    i % 2
                )

            lay.addLayout(grid)

        else:

            empty = QLabel(
                tr("no_milestones")
            )

            empty.setStyleSheet(
                f"font-size: 12px;"
                f"color: {TEXT_MUTED};"
                f"background: transparent;"
            )

            lay.addWidget(empty)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

    # =====================================================
    # Icon Button
    # =====================================================

    def _icon_button(self, text, danger=False):

        btn = QPushButton(text)
        btn.setFixedSize(28, 28)
        btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        hover_bg = (
            "rgba(224,92,92,0.2)"
            if danger
            else "rgba(255,255,255,0.1)"
        )

        btn.setStyleSheet(
            f"""
            QPushButton {{
                font-size: 13px;
                background: transparent;
                border: none;
            }}

            QPushButton:hover {{
                background: {hover_bg};
                border-radius: 8px;
            }}
            """
        )

        return btn

    # =====================================================
    # Milestone Widget
    # =====================================================

    def _milestone_widget(self, milestone):

        ms_card = QFrame()
        ms_card.setMinimumHeight(40)

        ms_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        ms_card.setStyleSheet(
            f"""
            QFrame {{
                background: rgba(
                    255,255,255,
                    {'0.1' if milestone.done else '0.05'}
                );
                border-radius: 8px;
            }}
            """
        )

        ml = QHBoxLayout(ms_card)
        ml.setContentsMargins(10, 8, 10, 8)
        ml.setSpacing(8)

        chk = QPushButton(
            "✅" if milestone.done else "⭕"
        )

        chk.setFixedSize(22, 22)

        chk.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        chk.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        chk.setStyleSheet(
            """
            QPushButton {
                font-size: 13px;
                background: transparent;
                border: none;
            }

            QPushButton:hover {
                background: rgba(255,255,255,0.1);
                border-radius: 6px;
            }
            """
        )

        chk.clicked.connect(
            lambda: self._handle_toggle_milestone(
                milestone.id
            )
        )

        nm = QLabel(
            tr(milestone.name)
        )

        nm.setWordWrap(True)

        nm.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        nm.setStyleSheet(
            f"""
            font-size: 12px;
            color: {
                TEXT_PRIMARY
                if milestone.done
                else TEXT_MUTED
            };
            background: transparent;
            {
                'text-decoration: line-through;'
                if milestone.done
                else ''
            }
            """
        )

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(20, 20)

        del_btn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        del_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        del_btn.setStyleSheet(
            f"""
            QPushButton {{
                font-size: 11px;
                color: {TEXT_MUTED};
                background: transparent;
                border: none;
            }}

            QPushButton:hover {{
                color: #e05c5c;
            }}
            """
        )

        del_btn.clicked.connect(
            lambda: self._handle_delete_milestone(
                milestone.id
            )
        )

        ml.addWidget(chk)
        ml.addWidget(nm, 1)
        ml.addWidget(del_btn)

        return ms_card

    # =====================================================
    # Handlers
    # =====================================================

    def _handle_edit(self):

        dialog = AddGoalDialog(
            self,
            goal=self.goal
        )

        if dialog.exec():

            data = dialog.result_data

            repo.update_goal(
                self.goal.id,
                data["name"],
                data["description"],
                data["icon"],
                data["category"],
                data["deadline"]
            )

            self.on_change()

    def _handle_delete(self):

        reply = QMessageBox.question(
            self,
            tr("delete_goal"),
            tr("delete_goal_confirm").format(
                name=tr(self.goal.name)
            ),
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            repo.delete_goal(
                self.goal.id
            )

            self.on_change()

    def _handle_add_milestone(self):

        dialog = AddMilestoneDialog(self)

        if dialog.exec():

            repo.add_milestone(
                self.goal.id,
                dialog.result_data["name"]
            )

            self.on_change()

    def _handle_toggle_milestone(self, milestone_id):

        repo.toggle_milestone(
            milestone_id
        )

        self.on_change()

    def _handle_delete_milestone(self, milestone_id):

        repo.delete_milestone(
            milestone_id
        )

        self.on_change()


# =========================================================
# Goals Page
# =========================================================

class GoalsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet(
            "background: transparent;"
        )

        # Selected filter
        self.selected_category = "All"

        self.scroll = QScrollArea(self)

        self.scroll.setWidgetResizable(True)

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.refresh()

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(self):

        content = QWidget()
        content.setStyleSheet(
            "background: transparent;"
        )

        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(
            28, 24, 28, 28
        )

        layout.addWidget(
            self._stats_row()
        )

        layout.addWidget(
            self._filter_row()
        )

        layout.addWidget(
            self._goals_list()
        )

        layout.addStretch()

        self.scroll.setWidget(content)

    # =====================================================
    # Stats
    # =====================================================

    def _stats_row(self):

        goals = repo.get_all_goals()

        # Apply selected category to stats
        if self.selected_category != "All":

            goals = [
                g for g in goals
                if g.category == self.selected_category
            ]

        total = len(goals)

        if goals:

            progresses = [
                repo.get_goal_progress_percent(g.id)
                for g in goals
            ]

            avg_progress = round(
                sum(progresses) / len(progresses)
            )

            completed = sum(
                1 for p in progresses
                if p == 100
            )

        else:

            avg_progress = 0
            completed = 0

        row = QWidget()
        row.setStyleSheet(
            "background: transparent;"
        )

        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [

            (
                "🎯",
                str(total),
                tr("goals"),
                tr("goals_in_progress"),
                ACCENT2,
                True
            ),

            (
                "✅",
                f"{avg_progress}%",
                tr("average_progress"),
                tr("across_all_goals"),
                GREEN,
                False
            ),

            (
                "🏆",
                str(completed),
                tr("progress"),
                tr("completed_this_year"),
                ORANGE,
                False
            ),

            (
                "📈",
                "+0%",
                tr("progress_rate"),
                tr("vs_last_month"),
                BLUE,
                False
            ),
        ]

        for (
            icon,
            val,
            title,
            sub,
            col,
            highlight
        ) in items:

            card = make_card(
                color="#1a1535"
                if highlight
                else BG_CARD
            )

            card.setMinimumHeight(120)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(
                18, 16, 18, 16
            )
            cl.setSpacing(6)

            top = QHBoxLayout()

            icon_box = QLabel(icon)
            icon_box.setFixedSize(40, 40)

            icon_box.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            icon_box.setStyleSheet(
                "font-size: 20px;"
                "background: rgba(255,255,255,0.07);"
                "border-radius: 10px;"
                "margin-bottom: 6px;"
            )

            top.addWidget(icon_box)
            top.addStretch()

            val_lbl = QLabel(val)
            val_lbl.setMinimumHeight(40)
            val_lbl.setStyleSheet(
                f"font-size: 30px;"
                f"font-weight: bold;"
                f"color: {TEXT_PRIMARY};"
                f"background: transparent;"
                f"padding-top: 6px;"
            )

            t_lbl = QLabel(title)
            t_lbl.setStyleSheet(
                f"font-size: 13px;"
                f"font-weight: 500;"
                f"color: {TEXT_PRIMARY};"
                f"background: transparent;"
            )

            s_lbl = QLabel(sub)
            s_lbl.setStyleSheet(
                f"font-size: 11px;"
                f"color: {TEXT_MUTED};"
                f"background: transparent;"
            )

            cl.addLayout(top)
            cl.addWidget(val_lbl)
            cl.addWidget(t_lbl)
            cl.addWidget(s_lbl)

            lay.addWidget(card)

        return row

    # =====================================================
    # Filter Row
    # =====================================================

    def _filter_row(self):

        goals = repo.get_all_goals()

        categories = [
            "All"
        ] + sorted(
            set(g.category for g in goals)
        )

        row = QWidget()
        row.setStyleSheet(
            "background: transparent;"
        )

        lay = QHBoxLayout(row)
        lay.setContentsMargins(
            0, 0, 0, 0
        )
        lay.setSpacing(8)

        for cat in categories:

            active = (
                cat == self.selected_category
            )

            btn = QPushButton(
                translate_goal_category(cat)
            )

            btn.setCheckable(True)
            btn.setChecked(active)

            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: {
                        ACCENT
                        if active
                        else 'transparent'
                    };

                    color: {
                        'white'
                        if active
                        else TEXT_MUTED
                    };

                    border: 1px solid {
                        'transparent'
                        if active
                        else 'rgba(255,255,255,0.12)'
                    };

                    border-radius: 16px;
                    padding: 6px 14px;
                    font-size: 12px;
                }}

                QPushButton:hover {{
                    background: rgba(
                        255,255,255,0.07
                    );
                    color: white;
                }}
                """
            )

            btn.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            btn.clicked.connect(
                lambda _, c=cat:
                self._select_category(c)
            )

            lay.addWidget(btn)

        lay.addStretch()

        return row

    # =====================================================
    # Select Category
    # =====================================================

    def _select_category(self, category):

        self.selected_category = category

        self.refresh()

    # =====================================================
    # Goals List
    # =====================================================

    def _goals_list(self):

        goals = repo.get_all_goals()

        # Apply filter
        if self.selected_category != "All":

            goals = [
                g for g in goals
                if g.category == self.selected_category
            ]

        col = QWidget()

        col.setStyleSheet(
            "background: transparent;"
        )

        col.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        lay = QVBoxLayout(col)
        lay.setContentsMargins(
            0, 0, 0, 0
        )
        lay.setSpacing(14)

        if not goals:

            empty_container = QWidget()

            empty_container.setStyleSheet(
                "background: transparent;"
            )

            empty_lay = QVBoxLayout(
                empty_container
            )

            empty_lay.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty_lay.setSpacing(12)

            empty_lay.setContentsMargins(
                40, 60, 40, 60
            )

            icon = QLabel("🎯")
            icon.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            icon.setStyleSheet(
                "font-size: 48px;"
                "background: transparent;"
            )

            empty_lay.addWidget(icon)

            title = QLabel(
                tr("empty_goals_title")
            )

            title.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            title.setStyleSheet(
                f"font-size: 18px;"
                f"font-weight: 600;"
                f"color: {TEXT_PRIMARY};"
                f"background: transparent;"
            )

            empty_lay.addWidget(title)

            desc = QLabel(
                tr("empty_goals_desc")
            )

            desc.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            desc.setStyleSheet(
                f"font-size: 13px;"
                f"color: {TEXT_MUTED};"
                f"background: transparent;"
            )

            desc.setWordWrap(True)

            empty_lay.addWidget(desc)

            lay.addWidget(
                empty_container
            )

        else:

            for i, goal in enumerate(goals):

                color, bg = GOAL_COLORS[
                    i % len(GOAL_COLORS)
                ]

                lay.addWidget(
                    GoalCard(
                        goal,
                        color,
                        bg,
                        on_change=self.refresh
                    )
                )

        # Add Goal
        add_card = QFrame()

        add_card.setMinimumHeight(80)

        add_card.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        add_card.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: 2px dashed
                    rgba(255,255,255,0.12);
                border-radius: 14px;
            }
            """
        )

        add_lay = QVBoxLayout(add_card)

        add_btn = QLabel(
            tr("add_new_goal")
        )

        add_btn.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        add_btn.setStyleSheet(
            f"font-size: 14px;"
            f"color: {TEXT_MUTED};"
            f"background: transparent;"
        )

        add_lay.addWidget(add_btn)

        add_card.mousePressEvent = (
            lambda event:
            self._open_add_dialog()
        )

        lay.addWidget(add_card)

        return col

    # =====================================================
    # Add Goal
    # =====================================================

    def _open_add_dialog(self):

        dialog = AddGoalDialog(self)

        if dialog.exec():

            data = dialog.result_data

            repo.add_goal(
                name=data["name"],
                description=data["description"],
                icon=data["icon"],
                category=data["category"],
                deadline=data["deadline"],
            )

            self.refresh()