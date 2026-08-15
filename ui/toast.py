from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

from assets.style import (
    BG_CARD, TEXT_PRIMARY, TEXT_MUTED,
    GREEN, ORANGE, ACCENT2,
)


class Toast(QFrame):
    """Toast notification — bottom-right overlay with fade in/out."""

    _active = None

    _KINDS = {
        "success":   (GREEN,   "rgba(62,207,142,0.15)",  "rgba(62,207,142,0.35)"),
        "milestone": (ORANGE,  "rgba(245,158,66,0.15)",  "rgba(245,158,66,0.35)"),
        "perfect":   (ACCENT2, "rgba(155,125,232,0.18)", "rgba(155,125,232,0.4)"),
        "info":      (TEXT_MUTED, "rgba(255,255,255,0.05)", "rgba(255,255,255,0.12)"),
    }

    def __init__(self, parent, title, message="", icon="✅", kind="success"):
        super().__init__(parent)
        self.setObjectName("smart_life_toast")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        accent, bg, border = self._KINDS.get(kind, self._KINDS["success"])
        self.setStyleSheet(f"""
            QFrame#smart_life_toast {{
                background: {BG_CARD};
                border: 1px solid {border};
                border-left: 4px solid {accent};
                border-radius: 12px;
            }}
        """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 14, 18, 14)
        lay.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setFixedWidth(28)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(
            f"font-size: 22px; background: {bg}; border-radius: 10px; padding: 4px;"
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet(
            f"font-size: 14px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;"
        )
        text_col.addWidget(title_lbl)

        if message:
            msg_lbl = QLabel(message)
            msg_lbl.setWordWrap(True)
            msg_lbl.setMaximumWidth(320)
            msg_lbl.setStyleSheet(
                f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;"
            )
            text_col.addWidget(msg_lbl)

        lay.addWidget(icon_lbl)
        lay.addLayout(text_col, 1)

        self.setFixedWidth(380)
        self.adjustSize()

        self._opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(0.0)

        self.mousePressEvent = lambda e: self.dismiss()

    def _reposition(self):
        parent = self.parentWidget()
        if not parent:
            return
        margin = 28
        x = max(margin, parent.width() - self.width() - margin)
        y = max(margin, parent.height() - self.height() - margin)
        self.move(x, y)

    def show_animated(self, duration_ms=3500):
        if Toast._active and Toast._active is not self:
            Toast._active.dismiss(immediate=True)

        Toast._active = self
        self._reposition()
        super().show()
        self.raise_()

        fade_in = QPropertyAnimation(self._opacity, b"opacity", self)
        fade_in.setDuration(220)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_in.start()
        self._fade_in = fade_in

        QTimer.singleShot(duration_ms, self.dismiss)

    def dismiss(self, immediate=False):
        if Toast._active is self:
            Toast._active = None

        if immediate:
            self.close()
            self.deleteLater()
            return

        fade_out = QPropertyAnimation(self._opacity, b"opacity", self)
        fade_out.setDuration(180)
        fade_out.setStartValue(self._opacity.opacity())
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        fade_out.finished.connect(lambda: (self.close(), self.deleteLater()))
        fade_out.start()
        self._fade_out = fade_out

    @classmethod
    def show(cls, parent, title, message="", icon="✅", kind="success", duration_ms=3500):
        if parent is None:
            return None
        toast = cls(parent, title, message, icon, kind)
        toast.show_animated(duration_ms)
        return toast
