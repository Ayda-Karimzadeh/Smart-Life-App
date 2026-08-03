import re

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

repo = goal_repo

# پالت رنگ‌ها برای چرخش بین اهداف
GOAL_COLORS = [
    (ACCENT2, "#1a1535"),
    (ORANGE,  "#2a1a0a"),
    (BLUE,    "#0a1a2a"),
    (GREEN,   "#0a2a1a"),
    (ACCENT,  "#1a1535"),
]


def _days_left(deadline_str):
    if not deadline_str:
        return None
    try:
        d = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        return (d - date.today()).days
    except ValueError:
        return None


# ─── کارت هدف ────────────────────────────────────────────────────────────────
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
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(22, 20, 22, 20)
        lay.setSpacing(12)

        # ─ ردیف بالا: آیکون + اطلاعات + درصد + دکمه‌ها ─
        top = QHBoxLayout()

        icon_box = QLabel(goal.icon)
        icon_box.setFixedSize(50, 50)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet("font-size: 24px; background: rgba(255,255,255,0.1); border-radius: 14px;")

        info = QVBoxLayout()
        info.setSpacing(4)
        name_lbl = QLabel(goal.name)
        name_lbl.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        desc_lbl = QLabel(goal.description)
        desc_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        desc_lbl.setWordWrap(True)

        tags = QHBoxLayout()
        tags.setSpacing(8)
        cat_lbl = QLabel(goal.category)
        cat_lbl.setStyleSheet(f"""
            font-size: 11px; color: {TEXT_PRIMARY};
            background: rgba(255,255,255,0.12);
            border-radius: 6px; padding: 2px 10px;
        """)
        tags.addWidget(cat_lbl)

        if days_left is not None:
            if days_left < 0:
                days_text = f"📅 {abs(days_left)} {tr('days_overdue')}"
            elif days_left == 0:
                days_text = f"📅 {tr('due_today')}"
            else:
                days_text = f"📅 {days_left} {tr('days_left')}"
            days_lbl = QLabel(days_text)
            days_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            tags.addWidget(days_lbl)

        tags.addStretch()

        info.addWidget(name_lbl)
        if goal.description:
            info.addWidget(desc_lbl)
        info.addLayout(tags)

        pct_col = QVBoxLayout()
        pct_col.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        pct_lbl = QLabel(f"{progress}%")
        pct_lbl.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color}; background: transparent;")
        pct_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        complete_lbl = QLabel(tr("progress").capitalize())
        complete_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        complete_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        pct_col.addWidget(pct_lbl)
        pct_col.addWidget(complete_lbl)

        # دکمه‌های ویرایش / حذف
        actions = QHBoxLayout()
        actions.setSpacing(4)
        edit_btn = self._icon_button("✏️")
        edit_btn.clicked.connect(self._handle_edit)
        delete_btn = self._icon_button("🗑️", danger=True)
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

        # ─ Progress Bar ─
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(progress)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        bar.setStyleSheet(f"""
            QProgressBar {{ background: rgba(255,255,255,0.1); border-radius: 4px; }}
            QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}
        """)
        lay.addWidget(bar)

        # ─ Milestones ─
        done_count = sum(1 for m in milestones if m.done)
        ms_header = QHBoxLayout()
        ms_lbl = QLabel(tr("milestones").capitalize())
        ms_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ms_count = QLabel(tr("milestones_completed").format(done=done_count,total=len(milestones),))
        ms_count.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

        add_ms_btn = QPushButton("+ " + tr("add"))
        add_ms_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_ms_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,255,255,0.08);
                color: {TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: 3px 12px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.15); }}
        """)
        add_ms_btn.clicked.connect(self._handle_add_milestone)

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
                grid.addWidget(self._milestone_widget(m), i // 2, i % 2)
            lay.addLayout(grid)
        else:
            empty = QLabel(tr("no_milestones"))
            empty.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            lay.addWidget(empty)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    # ─ دکمه آیکونی کوچک ──────────────────────────────────────────────────────
    def _icon_button(self, text, danger=False):
        btn = QPushButton(text)
        btn.setFixedSize(28, 28)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        hover_bg = "rgba(224,92,92,0.2)" if danger else "rgba(255,255,255,0.1)"
        btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 13px;
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background: {hover_bg};
                border-radius: 8px;
            }}
        """)
        return btn

    # ─ آیتم مایلستون (قابل کلیک برای toggle، با دکمه حذف) ─────────────────────
    def _milestone_widget(self, milestone):
        ms_card = QFrame()
        ms_card.setMinimumHeight(40)
        ms_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        ms_card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255,255,255,{'0.1' if milestone.done else '0.05'});
                border-radius: 8px;
            }}
        """)
        ml = QHBoxLayout(ms_card)
        ml.setContentsMargins(10, 8, 10, 8)
        ml.setSpacing(8)

        chk = QPushButton("✅" if milestone.done else "⭕")
        chk.setFixedSize(22, 22)
        chk.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        chk.setCursor(Qt.CursorShape.PointingHandCursor)
        chk.setStyleSheet("""
            QPushButton { font-size: 13px; background: transparent; border: none; }
            QPushButton:hover { background: rgba(255,255,255,0.1); border-radius: 6px; }
        """)
        chk.clicked.connect(lambda: self._handle_toggle_milestone(milestone.id))

        nm = QLabel(milestone.name)
        nm.setWordWrap(True)
        nm.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        nm.setStyleSheet(f"""
            font-size: 12px;
            color: {TEXT_PRIMARY if milestone.done else TEXT_MUTED};
            background: transparent;
            {'text-decoration: line-through;' if milestone.done else ''}
        """)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(20, 20)
        del_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet(f"""
            QPushButton {{ font-size: 11px; color: {TEXT_MUTED}; background: transparent; border: none; }}
            QPushButton:hover {{ color: #e05c5c; }}
        """)
        del_btn.clicked.connect(lambda: self._handle_delete_milestone(milestone.id))

        ml.addWidget(chk)
        ml.addWidget(nm, 1)
        ml.addWidget(del_btn)
        return ms_card

    # ─ Handlers ──────────────────────────────────────────────────────────────
    def _handle_edit(self):
        dialog = AddGoalDialog(self, goal=self.goal)
        if dialog.exec():
            data = dialog.result_data
            repo.update_goal(
                self.goal.id, data["name"], data["description"],
                data["icon"], data["category"], data["deadline"]
            )
            self.on_change()

    def _handle_delete(self):
        reply = QMessageBox.question(
            self, tr("delete_goal"),
            tr("delete_goal_confirm").format(name=self.goal.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            repo.delete_goal(self.goal.id)
            self.on_change()

    def _handle_add_milestone(self):
        dialog = AddMilestoneDialog(self)
        if dialog.exec():
            repo.add_milestone(self.goal.id, dialog.result_data["name"])
            self.on_change()

    def _handle_toggle_milestone(self, milestone_id):
        repo.toggle_milestone(milestone_id)
        self.on_change()

    def _handle_delete_milestone(self, milestone_id):
        repo.delete_milestone(milestone_id)
        self.on_change()


# ─── صفحه: Goals ─────────────────────────────────────────────────────────────
class GoalsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.refresh()

    # ─ بازسازی کامل صفحه با داده‌های تازه از دیتابیس ───────────────────────────
    def refresh(self):
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        layout.addWidget(self._stats_row())
        layout.addWidget(self._goals_list())
        layout.addStretch()

        self.scroll.setWidget(content)

    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        goals = repo.get_all_goals()
        total = len(goals)

        if goals:
            progresses = [repo.get_goal_progress_percent(g.id) for g in goals]
            avg_progress = round(sum(progresses) / len(progresses))
            completed = sum(1 for p in progresses if p == 100)
        else:
            avg_progress, completed = 0, 0

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("🎯", str(total), tr("goals").capitalize(), tr("goals_in_progress"), ACCENT2, True),
            ("✅", f"{avg_progress}%", tr("average_progress"), tr("across_all_goals"), GREEN, False),
            ("🏆", str(completed), tr("progress").capitalize(), tr("completed_this_year"), ORANGE, False),
            ("📈", "+0%", tr("progress_rate"), tr("vs_last_month"), BLUE, False),
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
            icon_box.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px;")
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

    # ─ لیست اهداف ─────────────────────────────────────────────────────────────
    def _goals_list(self):
        goals = repo.get_all_goals()

        col = QWidget()
        col.setStyleSheet("background: transparent;")
        col.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        lay = QVBoxLayout(col)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        if not goals:
            empty_container = QWidget()
            empty_container.setStyleSheet("background: transparent;")
            empty_lay = QVBoxLayout(empty_container)
            empty_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lay.setSpacing(12)
            empty_lay.setContentsMargins(40, 60, 40, 60)

            icon = QLabel("🎯")
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet("font-size: 48px; background: transparent;")
            empty_lay.addWidget(icon)

            title = QLabel(tr("empty_goals_title"))
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
            empty_lay.addWidget(title)

            desc = QLabel(tr("empty_goals_desc"))
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
            desc.setWordWrap(True)
            empty_lay.addWidget(desc)

            lay.addWidget(empty_container)
        else:
            for i, goal in enumerate(goals):
                color, bg = GOAL_COLORS[i % len(GOAL_COLORS)]
                lay.addWidget(GoalCard(goal, color, bg, on_change=self.refresh))

        # دکمه Add Goal
        add_card = QFrame()
        add_card.setMinimumHeight(80)
        add_card.setCursor(Qt.CursorShape.PointingHandCursor)
        add_card.setStyleSheet("QFrame { background: transparent; border: 2px dashed rgba(255,255,255,0.12); border-radius: 14px; }")
        add_lay = QVBoxLayout(add_card)
        add_btn = QLabel(tr("add_new_goal"))
        add_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_btn.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        add_lay.addWidget(add_btn)
        add_card.mousePressEvent = lambda event: self._open_add_dialog()
        lay.addWidget(add_card)

        return col

    # ─ باز کردن دیالوگ افزودن هدف ────────────────────────────────────────────
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