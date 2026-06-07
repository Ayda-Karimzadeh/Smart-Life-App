from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QFrame, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QTime

from assets.style import (
    BG_SIDEBAR, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT
)
class Sidebar(QWidget):
    def __init__(self, on_select):
        super().__init__()
        self.setFixedWidth(220)
        self.setStyleSheet(f"background-color: {BG_SIDEBAR}; border-right: 1px solid rgba(255,255,255,0.05);")
        self.buttons = []
        self.on_select = on_select

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 20, 12, 20)
        lay.setSpacing(4)

        # لوگو
        logo = QLabel("✦  Smart Life")
        logo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {TEXT_PRIMARY}; padding: 8px 12px 4px 12px;")
        sub = QLabel("Dashboard")
        sub.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; padding: 0 12px 18px 12px;")
        lay.addWidget(logo)
        lay.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: rgba(255,255,255,0.07);")
        lay.addWidget(sep)
        lay.addSpacing(8)

        pages = [
            ("📊", "Dashboard"),
            ("✅", "Habits"),
            ("🎯", "Goals"),
            ("📝", "Tasks"),
            ("⏱", "Time Tracking"),
            ("📈", "Analytics"),
        ]

        for i, (icon, name) in enumerate(pages):
            btn = QPushButton(f"  {icon}   {name}")
            btn.setCheckable(True)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(False))
            btn.clicked.connect(lambda _, idx=i: self._select(idx))
            lay.addWidget(btn)
            self.buttons.append(btn)

        lay.addStretch()

        # ساعت
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; padding: 8px;")
        lay.addWidget(self.clock)
        self._update_clock()
        timer = QTimer(self)
        timer.timeout.connect(self._update_clock)
        timer.start(1000)

        self._select(0)

    def _update_clock(self):
        self.clock.setText(QTime.currentTime().toString("hh:mm:ss"))

    def _select(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == idx)
            btn.setStyleSheet(self._btn_style(i == idx))
        self.on_select(idx)

    def _btn_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background: {ACCENT};
                    color: {TEXT_PRIMARY};
                    border-radius: 10px;
                    text-align: left;
                    padding-left: 12px;
                    font-size: 13px;
                    font-weight: 600;
                    border: none;
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_MUTED};
                border-radius: 10px;
                text-align: left;
                padding-left: 12px;
                font-size: 13px;
                font-weight: 400;
                border: none;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,0.05);
                color: {TEXT_PRIMARY};
            }}
        """
