from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from assets.style import (
    BG_CARD, BG_CARD2,
    TEXT_PRIMARY, TEXT_MUTED,
    GREEN, ORANGE, RED,
    make_card
)

class TasksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 28)
        lay.setSpacing(14)

        title = QLabel("Task Management")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        tasks = [
            ("📝", "گزارش هفتگی", "High", True, RED),
            ("💻", "کد پروژه PyQt6", "High", False, RED),
            ("📖", "مطالعه فصل ۵", "Medium", False, ORANGE),
            ("🏃", "ورزش بعدازظهر", "Low", True, GREEN),
            ("📧", "پاسخ به ایمیل‌ها", "Medium", False, ORANGE),
        ]

        for icon, name, prio, done, col in tasks:
            card = make_card(color=BG_CARD if not done else BG_CARD2)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(18, 14, 18, 14)

            check = QLabel("✅" if done else "⬜")
            check.setStyleSheet("font-size: 18px; background: transparent;")
            check.setFixedWidth(28)

            name_lbl = QLabel(f"{icon}  {name}")
            name_lbl.setStyleSheet(f"""
                font-size: 14px;
                color: {TEXT_MUTED if done else TEXT_PRIMARY};
                background: transparent;
                {'text-decoration: line-through;' if done else ''}
            """)

            prio_lbl = QLabel(prio)
            prio_lbl.setStyleSheet(f"""
                color: {col};
                background: rgba(255,255,255,0.05);
                border: 1px solid {col};
                border-radius: 8px;
                padding: 2px 10px;
                font-size: 11px;
                font-weight: 600;
            """)
            prio_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prio_lbl.setFixedWidth(70)

            cl.addWidget(check)
            cl.addWidget(name_lbl, 1)
            cl.addWidget(prio_lbl)
            lay.addWidget(card)

        lay.addStretch()