from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QFrame, QProgressBar, QGridLayout
)
from PyQt6.QtCore import Qt

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE,
    make_card
)


# ─── کارت هدف ────────────────────────────────────────────────────────────────
class GoalCard(QWidget):
    def __init__(self, icon, name, desc, category, days_left,
                 progress, milestones, color, bg_color, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        card = make_card(color=bg_color)
        card.setMinimumHeight(200)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(22, 20, 22, 20)
        lay.setSpacing(12)

        # ─ ردیف بالا: آیکون + اطلاعات + درصد ─
        top = QHBoxLayout()

        icon_box = QLabel(icon)
        icon_box.setFixedSize(50, 50)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet(f"""
            font-size: 24px;
            background: rgba(255,255,255,0.1);
            border-radius: 14px;
        """)

        info = QVBoxLayout()
        info.setSpacing(4)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
        desc_lbl.setWordWrap(True)

        tags = QHBoxLayout()
        tags.setSpacing(8)
        cat_lbl = QLabel(category)
        cat_lbl.setStyleSheet(f"""
            font-size: 11px; color: {TEXT_PRIMARY};
            background: rgba(255,255,255,0.12);
            border-radius: 6px; padding: 2px 10px;
        """)
        days_lbl = QLabel(f"📅 {days_left} days left")
        days_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        tags.addWidget(cat_lbl)
        tags.addWidget(days_lbl)
        tags.addStretch()

        info.addWidget(name_lbl)
        info.addWidget(desc_lbl)
        info.addLayout(tags)

        pct_col = QVBoxLayout()
        pct_col.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        pct_lbl = QLabel(f"{progress}%")
        pct_lbl.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color}; background: transparent;")
        pct_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        complete_lbl = QLabel("Complete")
        complete_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        complete_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        pct_col.addWidget(pct_lbl)
        pct_col.addWidget(complete_lbl)

        top.addWidget(icon_box)
        top.addSpacing(12)
        top.addLayout(info, 1)
        top.addLayout(pct_col)
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
        done_count = sum(1 for _, d in milestones if d)
        ms_header = QHBoxLayout()
        ms_lbl = QLabel("Milestones")
        ms_lbl.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ms_count = QLabel(f"{done_count} of {len(milestones)} completed")
        ms_count.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        ms_header.addWidget(ms_lbl)
        ms_header.addStretch()
        ms_header.addWidget(ms_count)
        lay.addLayout(ms_header)

        grid = QGridLayout()
        grid.setSpacing(8)
        for i, (ms_name, ms_done) in enumerate(milestones):
            ms_card = QFrame()
            ms_card.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255,255,255,{'0.1' if ms_done else '0.05'});
                    border-radius: 8px;
                }}
            """)
            ml = QHBoxLayout(ms_card)
            ml.setContentsMargins(10, 8, 10, 8)
            ml.setSpacing(8)

            chk = QLabel("✅" if ms_done else "⭕")
            chk.setStyleSheet("font-size: 14px; background: transparent;")
            chk.setFixedWidth(20)

            nm = QLabel(ms_name)
            nm.setStyleSheet(f"""
                font-size: 12px;
                color: {TEXT_PRIMARY if ms_done else TEXT_MUTED};
                background: transparent;
                {'text-decoration: line-through;' if ms_done else ''}
            """)

            ml.addWidget(chk)
            ml.addWidget(nm, 1)
            grid.addWidget(ms_card, i // 2, i % 2)

        lay.addLayout(grid)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)


# ─── صفحه: Goals ─────────────────────────────────────────────────────────────
class GoalsPage(QWidget):
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
        layout.addWidget(self._goals_list())
        layout.addStretch()

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    # ─ ۴ کارت آمار ───────────────────────────────────────────────────────────
    def _stats_row(self):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("🎯", "6", "Active Goals", "In progress", ACCENT2, True),
            ("✅", "50%", "Average Progress", "Across all goals", GREEN, False),
            ("🏆", "0", "Completed", "This year", ORANGE, False),
            ("📈", "+18%", "Progress Rate", "vs last month", BLUE, False),
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
            val_lbl.setStyleSheet(
                f"font-size: 30px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
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
        col = QWidget()
        col.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(col)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        goals = [
            (
                "🎯", "Learn Full-Stack Web Development",
                "Master React, Node.js, and databases to build complete web applications",
                "Learning", 119, 68, ACCENT2, "#1a1535",
                [
                    ("Complete React fundamentals", True),
                    ("Build 3 projects", True),
                    ("Learn Node.js & Express", True),
                    ("Database design & MongoDB", False),
                    ("Deploy full-stack app", False),
                ]
            ),
            (
                "🏃", "Run 100km This Month",
                "Improve cardiovascular health and endurance through consistent running",
                "Fitness", 27, 72, ORANGE, "#2a1a0a",
                [
                    ("Run 20km first week", True),
                    ("Run 25km second week", True),
                    ("Complete 10k race", False),
                    ("Run 100km total", False),
                ]
            ),
            # ← اینا رو اضافه کن
            (
                "🚀", "Launch SaaS Product",
                "Build and ship a SaaS product from idea to launch",
                "Career", 73, 47, ACCENT, "#1a1535",
                [
                    ("Validate idea & research", True),
                    ("Design MVP features", True),
                    ("Build core functionality", False),
                    ("Beta testing", False),
                    ("Public launch", False),
                ]
            ),
            (
                "🌍", "Master Spanish",
                "Achieve conversational fluency in Spanish",
                "Learning", 365, 28, BLUE, "#0a1a2a",
                [
                    ("Complete beginner course", True),
                    ("Practice 100 days", False),
                    ("Hold 10 conversations", False),
                    ("Pass fluency test", False),
                ]
            ),
        ]

        for g in goals:
            icon, name, desc, cat, days, pct, col_accent, bg, milestones = g
            lay.addWidget(GoalCard(icon, name, desc, cat, days, pct, milestones, col_accent, bg))

        add_card = QFrame()
        add_card.setMinimumHeight(80)
        add_card.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: 2px dashed rgba(255,255,255,0.12);
                border-radius: 14px;
            }}
        """)
        add_lay = QVBoxLayout(add_card)
        add_btn = QLabel("+ Add New Goal")
        add_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_btn.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; background: transparent;")
        add_lay.addWidget(add_btn)
        lay.addWidget(add_card)

        return col
