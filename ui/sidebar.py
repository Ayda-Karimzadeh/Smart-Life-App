from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QFrame, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QTime

from assets.style import (
    BG_SIDEBAR, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT
)
from core.language_manager import tr

class Sidebar(QWidget):
    def __init__(self, on_select, on_settings=None):
        super().__init__()
        self.setFixedWidth(220)
        self.setStyleSheet(f"background-color: {BG_SIDEBAR}; border-right: 1px solid rgba(255,255,255,0.05);")
        self.buttons = []
        self.on_select = on_select
        self.on_settings = on_settings

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 20, 12, 20)
        lay.setSpacing(4)

        # لوگو
        self.logo = QLabel("✦  Smart Life")
        self.logo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {TEXT_PRIMARY}; padding: 8px 12px 4px 12px;")
        self.sub = QLabel("Dashboard")
        self.sub.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; padding: 0 12px 18px 12px;")
        lay.addWidget(self.logo)
        lay.addWidget(self.sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: rgba(255,255,255,0.07);")
        lay.addWidget(sep)
        lay.addSpacing(8)

        self.page_icons = ["📊", "✅", "🎯", "�", "⏱", "📈"]
        self.page_keys = ["dashboard", "habits", "goals", "tasks", "time_tracking", "analytics"]

        for i, (icon, key) in enumerate(zip(self.page_icons, self.page_keys)):
            btn = QPushButton(f"  {icon}   {tr(key)}")
            btn.setCheckable(True)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(False))
            btn.clicked.connect(lambda _, idx=i: self._select(idx))
            lay.addWidget(btn)
            self.buttons.append(btn)

        lay.addStretch()

        # Settings button
        settings_btn = QPushButton(f"  ⚙️   {tr('settings')}")
        settings_btn.setCheckable(False)
        settings_btn.setFixedHeight(42)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #888899;
                border-radius: 10px;
                text-align: left;
                padding-left: 12px;
                font-size: 13px;
                font-weight: 400;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.05);
                color: #f0eeff;
            }
        """)
        if self.on_settings:
            settings_btn.clicked.connect(self.on_settings)
        lay.addWidget(settings_btn)

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

    def update_translations(self):
        """Update all text with current language translations"""
        self.sub.setText(tr("dashboard"))
        for i, (icon, key) in enumerate(zip(self.page_icons, self.page_keys)):
            self.buttons[i].setText(f"  {icon}   {tr(key)}")

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
