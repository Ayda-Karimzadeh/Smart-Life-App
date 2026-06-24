import matplotlib
matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

# ─── رنگ‌های ثابت (هماهنگ با style.py) ──────────────────────────────────────
BG      = "#0f0f14"
BG_CARD = "#1e1e2a"
FG      = "#f0eeff"
MUTED   = "#888899"
ACCENT  = "#7c5cbf"
ACCENT2 = "#9b7de8"
GREEN   = "#3ecf8e"
ORANGE  = "#f59e42"
BLUE    = "#4fa3e0"
RED     = "#e05c5c"

CAT_COLORS = {
    "Study":    ACCENT2,
    "Work":     BLUE,
    "Fitness":  GREEN,
    "Personal": ORANGE,
    "Other":    RED,
}


def _apply_dark_style(ax, fig):
    """استایل تاریک مشترک برای همه نمودارها"""
    fig.patch.set_facecolor(BG_CARD)
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.spines["bottom"].set_color(MUTED)
    ax.spines["left"].set_color(MUTED)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(FG)


# ─── کلاس پایه ───────────────────────────────────────────────────────────────
class BaseChart(QWidget):
    def __init__(self, width=5, height=3, parent=None):
        super().__init__(parent)
        self.fig = Figure(figsize=(width, height), tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.canvas)

    def redraw(self):
        self.canvas.draw()


# ─── ۱. نمودار خطی (Line Chart) ──────────────────────────────────────────────
class MplLineChart(BaseChart):
    """
    نمودار خطی با نقاط و سطح پر.
    کاربرد: Habit Score Trend، Focus Hours Trend
    """
    def __init__(self, data=None, labels=None, color=ACCENT2,
                 filled=True, ylabel="", parent=None):
        super().__init__(parent=parent)
        self.data   = data   or []
        self.labels = labels or []
        self.color  = color
        self.filled = filled
        self.ylabel = ylabel
        self._draw()

    def update_data(self, data, labels=None):
        self.data = data
        if labels:
            self.labels = labels
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        if not self.data:
            return

        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        x = range(len(self.data))

        if self.filled:
            ax.fill_between(x, self.data, alpha=0.2, color=self.color)

        ax.plot(x, self.data, color=self.color, linewidth=2.5,
                marker="o", markersize=6,
                markerfacecolor=self.color, markeredgecolor=BG_CARD,
                markeredgewidth=2)

        # خطوط راهنما
        ax.yaxis.grid(True, color=MUTED, alpha=0.2, linewidth=0.5)
        ax.set_axisbelow(True)

        if self.labels:
            ax.set_xticks(list(x))
            ax.set_xticklabels(self.labels, color=MUTED, fontsize=8)

        if self.ylabel:
            ax.set_ylabel(self.ylabel, color=MUTED, fontsize=9)

        ax.set_xlim(-0.3, len(self.data) - 0.7)


# ─── ۲. نمودار میله‌ای (Bar Chart) ───────────────────────────────────────────
class MplBarChart(BaseChart):
    """
    نمودار میله‌ای ساده.
    کاربرد: Weekly Activity در Timer Page
    """
    def __init__(self, data=None, color=GREEN, ylabel="Hours", parent=None):
        super().__init__(parent=parent)
        self.data   = data   or []
        self.color  = color
        self.ylabel = ylabel
        self._draw()

    def update_data(self, data):
        self.data = data
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        if not self.data:
            return

        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        x      = range(len(labels))

        bars = ax.bar(x, values, color=self.color, alpha=0.85,
                      width=0.5, zorder=3)

        # رنگ بار امروز
        today_idx = None
        from datetime import date
        day_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
                   "Fri": 4, "Sat": 5, "Sun": 6}
        today_name = date.today().strftime("%a")
        if today_name in day_map:
            today_idx = day_map[today_name]
            if today_idx < len(bars):
                bars[today_idx].set_color(ACCENT2)
                bars[today_idx].set_alpha(1.0)

        ax.yaxis.grid(True, color=MUTED, alpha=0.2, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, color=MUTED, fontsize=8)
        ax.set_ylabel(self.ylabel, color=MUTED, fontsize=9)
        ax.set_xlim(-0.5, len(labels) - 0.5)


# ─── ۳. نمودار دونات (Donut Chart) ───────────────────────────────────────────
class MplDonutChart(BaseChart):
    """
    نمودار دونات برای توزیع زمان.
    کاربرد: Time Distribution در Timer Page
    """
    def __init__(self, data=None, parent=None):
        super().__init__(width=4, height=4, parent=parent)
        self.data = data or []
        self._draw()

    def update_data(self, data):
        self.data = data
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        self.fig.patch.set_facecolor(BG_CARD)

        if not self.data or sum(v for _, v, _ in self.data) == 0:
            ax = self.fig.add_subplot(111)
            ax.set_facecolor(BG_CARD)
            ax.text(0.5, 0.5, "No data yet", ha="center", va="center",
                    color=MUTED, fontsize=11,
                    transform=ax.transAxes)
            ax.axis("off")
            return

        ax = self.fig.add_subplot(111)
        ax.set_facecolor(BG_CARD)

        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        colors = [d[2] for d in self.data]

        wedges, _ = ax.pie(
            values,
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.5, edgecolor=BG_CARD, linewidth=2),
        )

        # legend
        legend = ax.legend(
            wedges,
            [f"{l}  {v}h" for l, v in zip(labels, values)],
            loc="lower center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=2,
            frameon=False,
            fontsize=8,
            labelcolor=FG,
        )

        ax.set_aspect("equal")


# ─── ۴. نمودار مقایسه‌ای (Grouped Bar) ──────────────────────────────────────
class MplCompareBarChart(BaseChart):
    """
    نمودار میله‌ای مقایسه‌ای این هفته vs هفته قبل.
    کاربرد: Weekly Comparison در Analytics Page
    """
    def __init__(self, labels=None, this_week=None, last_week=None, parent=None):
        super().__init__(parent=parent)
        self.labels    = labels    or []
        self.this_week = this_week or []
        self.last_week = last_week or []
        self._draw()

    def update_data(self, labels, this_week, last_week):
        self.labels    = labels
        self.this_week = this_week
        self.last_week = last_week
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        if not self.labels:
            return

        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        x     = np.arange(len(self.labels))
        width = 0.35

        ax.bar(x - width/2, self.last_week, width,
               label="Last Week", color=MUTED, alpha=0.6, zorder=3)
        ax.bar(x + width/2, self.this_week, width,
               label="This Week", color=ACCENT2, alpha=0.9, zorder=3)

        ax.yaxis.grid(True, color=MUTED, alpha=0.2, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_xticks(x)
        ax.set_xticklabels(self.labels, color=MUTED, fontsize=8)
        ax.set_ylabel("Hours", color=MUTED, fontsize=9)

        legend = ax.legend(
            frameon=False, fontsize=8, labelcolor=FG,
            loc="upper left"
        )


# ─── ۵. نمودار رادار (Radar / Spider) ───────────────────────────────────────
class MplRadarChart(BaseChart):
    """
    نمودار رادار / عنکبوتی.
    کاربرد: Performance Radar در Analytics Page
    """
    def __init__(self, labels=None, values=None, parent=None):
        super().__init__(width=4, height=4, parent=parent)
        self.labels = labels or []
        self.values = values or []
        self._draw()

    def update_data(self, labels, values):
        self.labels = labels
        self.values = values
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        if not self.labels or not self.values:
            return

        self.fig.patch.set_facecolor(BG_CARD)

        n      = len(self.labels)
        angles = [i / n * 2 * np.pi for i in range(n)]
        angles += angles[:1]  # بستن چندضلعی

        vals = list(self.values) + [self.values[0]]

        ax = self.fig.add_subplot(111, polar=True)
        ax.set_facecolor(BG_CARD)

        # خطوط راهنما
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(["25", "50", "75", "100"],
                           color=MUTED, fontsize=7, alpha=0.5)
        ax.yaxis.grid(color=MUTED, alpha=0.2, linewidth=0.5)
        ax.xaxis.grid(color=MUTED, alpha=0.2, linewidth=0.5)

        # سطح داده
        ax.fill(angles, vals, color=ACCENT, alpha=0.25)
        ax.plot(angles, vals, color=ACCENT2, linewidth=2)
        ax.scatter(angles[:-1], vals[:-1],
                   color=ACCENT2, s=50, zorder=5,
                   edgecolors=BG_CARD, linewidth=2)

        # برچسب‌ها
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.labels, color=FG, fontsize=9)

        # پس‌زمینه
        ax.spines["polar"].set_color(MUTED)
        ax.spines["polar"].set_alpha(0.3)
        ax.tick_params(colors=MUTED)


# ─── ۶. نمودار Heatmap (Habit Calendar) ──────────────────────────────────────
class MplHabitHeatmap(BaseChart):
    """
    نمودار گرما (مثل GitHub contributions).
    کاربرد: نمایش فعالیت ۱۲ هفته گذشته در Analytics
    """
    def __init__(self, habit_id=None, parent=None):
        super().__init__(width=8, height=2, parent=parent)
        self.habit_id = habit_id
        self._draw()

    def update_habit(self, habit_id):
        self.habit_id = habit_id
        self.fig.clear()
        self._draw()
        self.redraw()

    def _draw(self):
        from datetime import date, timedelta
        from database import db_manager as db

        self.fig.patch.set_facecolor(BG_CARD)
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(BG_CARD)

        # ۱۲ هفته گذشته
        weeks  = 12
        today  = date.today()
        start  = today - timedelta(weeks=weeks)

        # grid: 7 روز × weeks هفته
        grid = np.zeros((7, weeks))

        if self.habit_id:
            conn = db.get_connection()
            rows = conn.execute(
                "SELECT log_date FROM habit_logs WHERE habit_id = ? AND log_date >= ?",
                (self.habit_id, start.isoformat())
            ).fetchall()
            conn.close()

            done_dates = {r[0] for r in rows}
            for col in range(weeks):
                for row in range(7):
                    d = start + timedelta(weeks=col, days=row)
                    if d.isoformat() in done_dates:
                        grid[row][col] = 1

        # رسم heatmap
        cmap = matplotlib.colors.ListedColormap([BG_CARD2, GREEN])
        ax.imshow(grid, cmap=cmap, aspect="auto", vmin=0, vmax=1)

        # برچسب‌های روز
        ax.set_yticks(range(7))
        ax.set_yticklabels(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
                           color=MUTED, fontsize=7)

        # برچسب هفته‌ها (هر ۴ هفته)
        week_labels = []
        for i in range(weeks):
            d = start + timedelta(weeks=i)
            week_labels.append(d.strftime("%b %d") if i % 4 == 0 else "")
        ax.set_xticks(range(weeks))
        ax.set_xticklabels(week_labels, color=MUTED, fontsize=7)

        ax.spines[:].set_visible(False)
        ax.tick_params(length=0)

      