import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QScrollArea, QPushButton,
    QComboBox, QDialog, QLineEdit, QSpinBox,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PyQt6.QtMultimedia import QSoundEffect

from assets.style import (
    BG_CARD, BG_CARD2, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, ACCENT2, GREEN, ORANGE, BLUE, RED,
    make_card
)
from ui.dialogs import EditSessionDialog
from database.repository import (
    goal_repo,
    habit_repo,
    task_repo,
    analytics_repo,
    time_repo,
)
from core.language_manager import tr

# نگاشت کلید انگلیسیِ ثابت (که در دیتابیس ذخیره می‌شود) به کلید ترجمه
CATEGORY_TR_KEYS = {
    "Study": "study",
    "Work": "work",
    "Fitness": "fitness",
    "Personal": "personal",
    "Other": "other",
}


def translate_category(category: str) -> str:
    """نام دسته‌بندی ذخیره‌شده به انگلیسی را به زبان جاری برنمی‌گرداند مگر با tr()"""
    key = CATEGORY_TR_KEYS.get(category)
    return tr(key) if key else category


# ─── نمودار میله‌ای ───────────────────────────────────────────────────────────
class BarChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or [("Mon", 0)] * 7
        self.setMinimumHeight(200)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 30
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b
        max_val = max((v for _, v in self.data), default=1) or 1
        bar_count = len(self.data)
        bar_w = int(chart_w / bar_count * 0.5)
        gap = chart_w / bar_count

        for i in range(5):
            y = pad_t + i * chart_h // 4
            p.setPen(QPen(QColor(50, 50, 70), 1))
            p.drawLine(pad_l, y, w - pad_r, y)
            val = max_val - i * max_val / 4
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(0, y - 6, pad_l - 4, 14,
                       Qt.AlignmentFlag.AlignRight, f"{val:.1f}")

        for i, (day, val) in enumerate(self.data):
            bar_h = int(val / max_val * chart_h) if max_val > 0 else 0
            x = int(pad_l + i * gap + (gap - bar_w) / 2)
            y = pad_t + chart_h - bar_h
            p.setBrush(QBrush(QColor(GREEN)))
            p.setPen(Qt.PenStyle.NoPen)
            if bar_h > 0:
                p.drawRoundedRect(x, y, bar_w, bar_h, 4, 4)
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(x - 5, h - pad_b + 6, bar_w + 10, 20,
                       Qt.AlignmentFlag.AlignHCenter, day)


# ─── نمودار دونات ─────────────────────────────────────────────────────────────
class DonutChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or []
        self.setMinimumSize(180, 180)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.data:
            p.setPen(QColor(TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 11))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No data yet")
            return
        size = min(self.width(), self.height()) - 20
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        total = sum(v for _, v, _ in self.data) or 1
        start = 90 * 16
        thickness = 28
        for _, val, color in self.data:
            span = int(val / total * 360 * 16)
            p.setPen(QPen(QColor(color), thickness,
                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.setBrush(Qt.BrushStyle.NoBrush)
            m = thickness // 2
            p.drawArc(x + m, y + m, size - thickness, size - thickness, start, -span)
            start -= span


# ─── دیالوگ شروع session با زمان دلخواه ──────────────────────────────────────
class StartSessionDialog(QDialog):
    """قبل از شروع تایمر: اسم، دسته و مدت زمان رو می‌گیره."""

    CATEGORIES = ["Study", "Work", "Fitness", "Personal", "Other"]
    PRESETS = [("25 min — Pomodoro", 25), ("45 min — Deep Work", 45),
               ("60 min — Focus", 60), ("90 min — Flow", 90), ("Custom", 0)]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("start_focus_session"))
        self.setFixedWidth(360)
        self.result_data = None

        self.setStyleSheet(f"QDialog {{ background: {BG_CARD}; color: {TEXT_PRIMARY}; }}")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel(tr("start_timer"))
        title.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        INPUT = f"""
            QLineEdit, QComboBox, QSpinBox {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; padding: 8px 12px; font-size: 13px;
            }}
            QComboBox QAbstractItemView {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                selection-background-color: {ACCENT};
            }}
        """

        # اسم session
        lay.addWidget(self._lbl(tr("session_name")))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(tr("session_name_placeholder"))
        self.name_edit.setStyleSheet(INPUT)
        lay.addWidget(self.name_edit)

        # دسته‌بندی
        lay.addWidget(self._lbl(tr("category")))

        self.cat_combo = QComboBox()

        self.cat_combo.addItem(tr("study"), "Study")
        self.cat_combo.addItem(tr("work"), "Work")
        self.cat_combo.addItem(tr("fitness"), "Fitness")
        self.cat_combo.addItem(tr("personal"), "Personal")
        self.cat_combo.addItem(tr("other"), "Other")

        self.cat_combo.setStyleSheet(INPUT)
        lay.addWidget(self.cat_combo)

        # preset زمان‌ها
        lay.addWidget(self._lbl(tr("duration")))
        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        self.preset_btns = []
        for label, mins in self.PRESETS:
            btn = QPushButton(label.split("—")[0].strip())
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._preset_style(False))
            btn.clicked.connect(lambda _, m=mins, b=btn: self._select_preset(m, b))
            preset_row.addWidget(btn)
            self.preset_btns.append((btn, mins))
        lay.addLayout(preset_row)

        # ورودی دقیقه دلخواه
        custom_row = QHBoxLayout()
        custom_row.setSpacing(8)

        self.min_spin = QSpinBox()
        self.min_spin.setRange(1, 480)
        self.min_spin.setValue(25)
        self.min_spin.setSuffix(" min")
        self.min_spin.setStyleSheet(INPUT)

        custom_label = QLabel(tr("custom_duration"))
        custom_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")

        custom_row.addWidget(custom_label)
        custom_row.addWidget(self.min_spin, 1)

        lay.addLayout(custom_row)

        # انتخاب پیش‌فرض اول
        self._select_preset(25, self.preset_btns[0][0])

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px; padding: 10px 0; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        start_btn = QPushButton("▶  " + tr("start"))
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white; border: none;
                border-radius: 10px; padding: 10px 0;
                font-size: 13px; font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        start_btn.clicked.connect(self._handle_start)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(start_btn, 1)
        lay.addLayout(btn_row)

    def _lbl(self, text):
        l = QLabel(text)
        l.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        return l

    def _preset_style(self, active):
        return f"""
            QPushButton {{
                background: {'%s' % ACCENT if active else 'rgba(255,255,255,0.07)'};
                color: {'white' if active else TEXT_MUTED};
                border: none; border-radius: 8px;
                padding: 6px 8px; font-size: 11px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.12); }}
        """

    def _select_preset(self, mins, active_btn):
        for btn, m in self.preset_btns:
            btn.setChecked(btn == active_btn)
            btn.setStyleSheet(self._preset_style(btn == active_btn))
        if mins > 0:
            self.min_spin.setValue(mins)

    def _handle_start(self):
        name = self.name_edit.text().strip() or self.cat_combo.currentText()
        self.result_data = {
            "name": name,
            "category": self.cat_combo.currentData(),
            "minutes": self.min_spin.value(),
        }
        self.accept()


# ─── دیالوگ ویرایش session ───────────────────────────────────────────────────
class EditSessionDialog(QDialog):
    CATEGORIES = ["Study", "Work", "Fitness", "Personal", "Other"]

    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle(tr("edit_session"))
        self.setFixedWidth(360)
        self.result_data = None

        self.setStyleSheet(f"QDialog {{ background: {BG_CARD}; color: {TEXT_PRIMARY}; }}")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        title = QLabel(tr("edit_session"))
        title.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {TEXT_PRIMARY};")
        lay.addWidget(title)

        INPUT = f"""
            QLineEdit, QComboBox, QSpinBox {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; padding: 8px 12px; font-size: 13px;
            }}
            QComboBox QAbstractItemView {{
                background: {BG_CARD2}; color: {TEXT_PRIMARY};
                selection-background-color: {ACCENT};
            }}
        """

        # نام
        name_lbl = QLabel(tr("session_name"))
        name_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        self.name_edit = QLineEdit(session.name)
        self.name_edit.setStyleSheet(INPUT)
        lay.addWidget(name_lbl)
        lay.addWidget(self.name_edit)

        # دسته‌بندی
        cat_lbl = QLabel(tr("category"))
        cat_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        self.cat_combo = QComboBox()

        # هر آیتم: متن ترجمه‌شده برای نمایش + کلید انگلیسی ثابت به‌عنوان data
        self.cat_combo.addItem(tr("study"), "Study")
        self.cat_combo.addItem(tr("work"), "Work")
        self.cat_combo.addItem(tr("fitness"), "Fitness")
        self.cat_combo.addItem(tr("personal"), "Personal")
        self.cat_combo.addItem(tr("other"), "Other")

        # پیدا کردن ایندکس بر اساس کلید انگلیسی ذخیره‌شده در session، نه متن ترجمه‌شده
        idx = self.cat_combo.findData(session.category)
        if idx >= 0:
            self.cat_combo.setCurrentIndex(idx)

        self.cat_combo.setStyleSheet(INPUT)
        lay.addWidget(cat_lbl)
        lay.addWidget(self.cat_combo)

        # مدت زمان (دقیقه و ثانیه جدا)
        dur_lbl = QLabel(tr("duration"))
        dur_lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED};")
        lay.addWidget(dur_lbl)

        dur_row = QHBoxLayout()
        dur_row.setSpacing(10)

        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 1440)
        self.min_spin.setValue(session.duration // 60)
        self.min_spin.setSuffix(" min")
        self.min_spin.setStyleSheet(INPUT)

        self.sec_spin = QSpinBox()
        self.sec_spin.setRange(0, 59)
        self.sec_spin.setValue(session.duration % 60)
        self.sec_spin.setSuffix(" sec")
        self.sec_spin.setStyleSheet(INPUT)

        dur_row.addWidget(self.min_spin, 1)
        dur_row.addWidget(self.sec_spin, 1)
        lay.addLayout(dur_row)

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {TEXT_MUTED};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px; padding: 10px 0; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.05); }}
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton(tr("save_changes"))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white; border: none;
                border-radius: 10px; padding: 10px 0;
                font-size: 13px; font-weight: 600;
            }}
            QPushButton:hover {{ background: {ACCENT2}; }}
        """)
        save_btn.clicked.connect(self._handle_save)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(save_btn, 1)
        lay.addLayout(btn_row)

    def _handle_save(self):
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setStyleSheet(
                self.name_edit.styleSheet() + "QLineEdit { border: 1px solid #e05c5c; }"
            )
            return
        total_secs = self.min_spin.value() * 60 + self.sec_spin.value()
        self.result_data = {
            "name": name,
            "category": self.cat_combo.currentData(),
            "duration_seconds": total_secs,
        }
        self.accept()


# ─── کارت session با دکمه‌های edit/delete ────────────────────────────────────
class SessionCard(QWidget):
    CAT_ICONS  = {"Study": "📖", "Work": "💼", "Fitness": "🏃", "Personal": "🧘", "Other": "⏱"}
    CAT_COLORS = {"Study": ACCENT2, "Work": BLUE, "Fitness": GREEN, "Personal": ORANGE, "Other": RED}

    def __init__(self, session, on_change, parent=None):
        super().__init__(parent)
        self.session   = session
        self.on_change = on_change
        self.setStyleSheet("background: transparent;")

        card = make_card(color=BG_CARD2)
        cl = QHBoxLayout(card)
        cl.setContentsMargins(16, 12, 16, 12)
        cl.setSpacing(14)

        # آیکون
        icon = self.CAT_ICONS.get(session.category, "⏱")
        icon_box = QLabel(icon)
        icon_box.setFixedSize(40, 40)
        icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_box.setStyleSheet("font-size: 20px; background: rgba(255,255,255,0.07); border-radius: 10px;")

        # اطلاعات
        info = QVBoxLayout()
        info.setSpacing(3)
        n = QLabel(session.name)
        n.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        t = QLabel(f"{translate_category(session.category)}  •  {session.session_date}")
        t.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        info.addWidget(n)
        info.addWidget(t)

        # مدت + دکمه‌ها
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        right_col.setSpacing(4)

        d = QLabel(session.duration_str)
        d.setAlignment(Qt.AlignmentFlag.AlignRight)
        d.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        dl = QLabel(tr("duration"))
        dl.setAlignment(Qt.AlignmentFlag.AlignRight)
        dl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")

        actions = QHBoxLayout()
        actions.setSpacing(4)
        actions.setAlignment(Qt.AlignmentFlag.AlignRight)

        edit_btn = self._icon_btn("✏️")
        edit_btn.clicked.connect(self._handle_edit)

        del_btn = self._icon_btn("🗑️", danger=True)
        del_btn.clicked.connect(self._handle_delete)

        actions.addWidget(edit_btn)
        actions.addWidget(del_btn)

        right_col.addLayout(actions)
        right_col.addWidget(d)
        right_col.addWidget(dl)

        cl.addWidget(icon_box)
        cl.addLayout(info, 1)
        cl.addLayout(right_col)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

    def _icon_btn(self, text, danger=False):
        btn = QPushButton(text)
        btn.setFixedSize(28, 28)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        hover = "rgba(224,92,92,0.2)" if danger else "rgba(255,255,255,0.1)"
        btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 13px; background: transparent; border: none;
            }}
            QPushButton:hover {{ background: {hover}; border-radius: 8px; }}
        """)
        return btn

    def _handle_edit(self):
        from ui.dialogs import EditSessionDialog
        dialog = EditSessionDialog(self.session, self)
        if dialog.exec():
            data = dialog.result_data
            time_repo.update_time_session(
                self.session.id,
                data["name"],
                data["category"],
                data["duration_seconds"],
            )
            self.on_change()

    def _handle_delete(self):
        reply = QMessageBox.question(
            self,
            tr("delete_session"),
            tr("delete_session_confirm").format(name=self.session.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            time_repo.delete_time_session(self.session.id)
            self.on_change()


# ─── صفحه: Time Tracking ─────────────────────────────────────────────────────
class TimerPage(QWidget):

    MODE_STOPWATCH  = "stopwatch"   # شمارش رو به جلو
    MODE_COUNTDOWN  = "countdown"   # شمارش معکوس

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self._seconds     = 0        # زمان فعلی
        self._target      = 0        # هدف (برای countdown)
        self._running     = False
        self._mode        = self.MODE_STOPWATCH
        self._session_name    = ""
        self._session_category = "Other"

        self._qt_timer = QTimer(self)
        self._qt_timer.timeout.connect(self._tick)

        # صدای اتمام — فایل beep.wav اگه نبود، از QApplication.beep استفاده می‌کنیم
        self._sound = QSoundEffect()
        beep_path = os.path.join(os.path.dirname(__file__), "beep.wav")
        if os.path.exists(beep_path):
            self._sound.setSource(QUrl.fromLocalFile(beep_path))

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(self.scroll)

        self.refresh()

    # ─ بازسازی صفحه ──────────────────────────────────────────────────────────
    def refresh(self):
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 24, 28, 28)

        layout.addWidget(self._stats_row())
        layout.addWidget(self._timer_banner())
        layout.addWidget(self._charts_row())
        layout.addWidget(self._recent_sessions())
        layout.addStretch()

        self.scroll.setWidget(content)

    # ─ آمار ──────────────────────────────────────────────────────────────────
    def _stats_row(self):
        total_today = time_repo.get_total_time_today()
        weekly      = time_repo.get_weekly_activity()
        total_week  = sum(h for _, h in weekly)
        dist        = time_repo.get_time_distribution()
        top_cat     = translate_category(max(dist, key=lambda x: x[1])[0]) if dist else "—"
        daily_avg   = round(total_week / 7, 1) if total_week else 0

        def fmt(secs):
            h = int(secs // 3600)
            m = int((secs % 3600) // 60)
            return f"{h}h {m}m" if h else f"{m}m"

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        items = [
            ("⏱", fmt(total_today), tr("focused_today"), tr("vs_yesterday"), ACCENT2, True),
            ("📈", f"{total_week:.1f}h", tr("this_week"), tr("across_all_categories"), BLUE, False),
            ("📖", top_cat, tr("top_category"), tr("most_time_spent"), ACCENT, False),
            ("📅", f"{daily_avg}h", tr("daily_average"), tr("this_week"), GREEN, False),
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
            val_lbl = QLabel(str(val))
            val_lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {TEXT_PRIMARY}; background: transparent;")
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

    # ─ بنر تایمر ─────────────────────────────────────────────────────────────
    def _timer_banner(self):
        card = make_card(color="#1a1535")
        card.setMinimumHeight(220)
        lay = QVBoxLayout(card)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)

        # نام session جاری
        self.session_info_lbl = QLabel("")
        self.session_info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session_info_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
        lay.addWidget(self.session_info_lbl)

        # نمایش زمان بزرگ
        self.time_lbl = QLabel("00:00:00")
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_lbl.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {ACCENT2}; background: transparent;")
        lay.addWidget(self.time_lbl)

        # progress bar برای countdown
        from PyQt6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{ background: rgba(255,255,255,0.08); border-radius: 3px; }}
            QProgressBar::chunk {{ background: {ACCENT2}; border-radius: 3px; }}
        """)
        self.progress_bar.hide()
        lay.addWidget(self.progress_bar)

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        btn_row.setSpacing(12)

        # دکمه Start Session (باز کردن دیالوگ)
        self.start_btn = QPushButton("▶  " + tr("start") + " " + tr("session_name"))
        self.start_btn.setFixedHeight(46)
        self.start_btn.setMinimumWidth(160)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet(self._btn_style(ACCENT, ACCENT2))
        self.start_btn.clicked.connect(self._handle_start_btn)

        # دکمه Stop
        self.stop_btn = QPushButton("⏹  " + tr("stop_timer") + " & " + tr("save"))
        self.stop_btn.setFixedHeight(46)
        self.stop_btn.setMinimumWidth(140)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setStyleSheet(self._btn_style(RED, "#c04040"))
        self.stop_btn.hide()
        self.stop_btn.clicked.connect(self._handle_stop)

        # دکمه Reset
        self.reset_btn = QPushButton("↺  " + tr("reset"))
        self.reset_btn.setFixedHeight(46)
        self.reset_btn.setMinimumWidth(100)
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,255,255,0.07); color: {TEXT_MUTED};
                border: none; border-radius: 14px; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.12); color: white; }}
        """)
        self.reset_btn.hide()
        self.reset_btn.clicked.connect(self._handle_reset)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.stop_btn)
        btn_row.addWidget(self.reset_btn)
        lay.addLayout(btn_row)

        return card

    def _btn_style(self, color, hover):
        return f"""
            QPushButton {{
                background: {color}; color: white; border: none;
                border-radius: 14px; font-size: 14px; font-weight: 600;
            }}
            QPushButton:hover {{ background: {hover}; }}
        """

    # ─ نمودارها ──────────────────────────────────────────────────────────────
    def _charts_row(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main_lay = QVBoxLayout(container)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(14)

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        weekly_data = time_repo.get_weekly_activity()
        left = make_card()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 18, 20, 18)
        ll.setSpacing(12)
        t1 = QLabel(tr("weekly_activity"))
        t1.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        ll.addWidget(t1)
        ll.addWidget(BarChart(weekly_data))

        legend = QHBoxLayout()
        legend.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        legend.setSpacing(16)
        for name, col in [("Study", ACCENT2), ("Work", BLUE), ("Fitness", ORANGE), ("Personal", GREEN)]:
            rl = QHBoxLayout()
            dot = QLabel("■")
            dot.setStyleSheet(f"color: {col}; background: transparent; font-size: 11px;")
            lbl = QLabel(translate_category(name))
            lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            rl.addWidget(dot)
            rl.addWidget(lbl)
            legend.addLayout(rl)
        ll.addLayout(legend)

        dist_data = time_repo.get_time_distribution()
        cat_colors = {"Study": ACCENT2, "Work": BLUE, "Fitness": GREEN, "Personal": ORANGE, "Other": RED}
        donut_data = [(cat, hrs, cat_colors.get(cat, ACCENT)) for cat, hrs in dist_data]

        right = make_card()
        rl2 = QVBoxLayout(right)
        rl2.setContentsMargins(20, 18, 20, 18)
        rl2.setSpacing(12)
        t2 = QLabel(tr("time_distribution"))
        t2.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        rl2.addWidget(t2)
        donut = DonutChart(donut_data)
        donut.setMinimumHeight(180)
        rl2.addWidget(donut)

        for cat, hrs, col in donut_data:
            r2 = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {col}; background: transparent; font-size: 12px;")
            dot.setFixedWidth(16)
            n = QLabel(translate_category(cat))
            n.setStyleSheet(f"font-size: 12px; color: {TEXT_PRIMARY}; background: transparent;")
            v = QLabel(f"{hrs}h")
            v.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            r2.addWidget(dot)
            r2.addWidget(n, 1)
            r2.addWidget(v)
            rl2.addLayout(r2)

        lay.addWidget(left, 2)
        lay.addWidget(right, 1)
        main_lay.addWidget(row)
        return container

    # ─ Recent Sessions ────────────────────────────────────────────────────────
    def _recent_sessions(self):
        sessions = time_repo.get_recent_sessions(limit=10)
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(section)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        title = QLabel(tr("recent_sessions"))
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        lay.addWidget(title)

        if not sessions:
            empty_container = QWidget()
            empty_container.setStyleSheet("background: transparent;")
            empty_lay = QVBoxLayout(empty_container)
            empty_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lay.setSpacing(8)
            empty_lay.setContentsMargins(20, 40, 20, 40)

            icon = QLabel("⏱️")
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet("font-size: 36px; background: transparent;")
            empty_lay.addWidget(icon)

            title = QLabel(tr("empty_timer_title"))
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
            empty_lay.addWidget(title)

            desc = QLabel(tr("empty_timer_desc"))
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setStyleSheet(f"font-size: 12px; color: {TEXT_MUTED}; background: transparent;")
            desc.setWordWrap(True)
            empty_lay.addWidget(desc)

            lay.addWidget(empty_container)
            return section

        for s in sessions:
            lay.addWidget(SessionCard(s, on_change=self.refresh))

        return section

    # ─ منطق تایمر ────────────────────────────────────────────────────────────
    def _handle_start_btn(self):
        """باز کردن دیالوگ تنظیم session"""
        if self._running:
            return

        dialog = StartSessionDialog(self)
        if not dialog.exec():
            return

        data = dialog.result_data
        self._session_name     = data["name"]
        self._session_category = data["category"]
        minutes                = data["minutes"]

        self._mode    = self.MODE_COUNTDOWN
        self._target  = minutes * 60
        self._seconds = self._target   # شمارش معکوس از target

        # آپدیت UI
        self.session_info_lbl.setText(
            f"⏱  {self._session_name}  •  {translate_category(self._session_category)}  •  {minutes} min"
        )
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self._update_display()

        # نمایش دکمه‌های مناسب
        self.start_btn.hide()
        self.stop_btn.show()
        self.reset_btn.show()

        self._running = True
        self._qt_timer.start(1000)

    def _handle_stop(self):
        """توقف و ذخیره session"""
        if not self._running:
            return
        self._qt_timer.stop()
        self._running = False

        # زمان واقعی که گذشته
        elapsed = self._target - self._seconds if self._mode == self.MODE_COUNTDOWN else self._seconds
        if elapsed >= 10:  # حداقل ۱۰ ثانیه
            time_repo.add_time_session(
                name=self._session_name,
                category=self._session_category,
                duration_seconds=elapsed,
            )

        self._reset_state()
        self.refresh()

    def _handle_reset(self):
        """ریست بدون ذخیره"""
        self._qt_timer.stop()
        self._running = False
        self._reset_state()

    def _reset_state(self):
        self._seconds = 0
        self._target  = 0
        self.time_lbl.setText("00:00:00")
        self.time_lbl.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {ACCENT2}; background: transparent;")
        self.session_info_lbl.setText("")
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.start_btn.show()
        self.stop_btn.hide()
        self.reset_btn.hide()

    def _tick(self):
        if self._mode == self.MODE_COUNTDOWN:
            self._seconds -= 1
            if self._seconds <= 0:
                self._seconds = 0
                self._update_display()
                self._on_countdown_done()
                return
            # رنگ قرمز وقتی کمتر از ۱ دقیقه مونده
            if self._seconds <= 60:
                self.time_lbl.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {RED}; background: transparent;")
            # progress bar
            pct = int((1 - self._seconds / self._target) * 100) if self._target else 0
            self.progress_bar.setValue(pct)
        else:
            self._seconds += 1

        self._update_display()

    def _update_display(self):
        secs = abs(self._seconds)
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        self.time_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def _on_countdown_done(self):
        """وقتی countdown به صفر رسید"""
        self._qt_timer.stop()
        self._running = False

        # پخش صدا
        if self._sound.source().isValid():
            self._sound.play()
        else:
            from PyQt6.QtWidgets import QApplication
            QApplication.beep()

        # پیام تبریک
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("✅ " + tr("session_complete"))
        msg.setText(
            f"<b>{self._session_name}</b> "
            f"{tr('session_finished')}<br>"
            f"{tr('duration_minutes')}: "
            f"<b>{self._target // 60}</b>"
        )
        msg.setStyleSheet(f"QMessageBox {{ background: {BG_CARD}; color: {TEXT_PRIMARY}; }}")
        msg.exec()

        # ذخیره خودکار
        time_repo.add_time_session(
            name=self._session_name,
            category=self._session_category,
            duration_seconds=self._target,
        )

        self._reset_state()
        self.refresh()