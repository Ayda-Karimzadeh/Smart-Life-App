import sys
import os

# اضافه کردن مسیر پروژه به Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

from database.db_manager import init_db
from database.repository import habit_repo


# ─── Seed Data — داده‌های اولیه اگه دیتابیس خالیه ───────────────────────────
def seed_data():
    """اگه دیتابیس خالیه، چند عادت نمونه اضافه می‌کنه."""
    if habit_repo.get_all_habits():
        return

    default_habits = [
        ("Morning Meditation", "🧘", "Mindfulness", "daily",  7),
        ("Exercise",           "💪", "Fitness",     "daily",  7),
        ("Reading",            "📚", "Personal Growth", "daily", 7),
        ("Drink 8 Glasses",    "💧", "Health",      "daily",  7),
        ("Practice Guitar",    "🎸", "Skills",      "weekly", 3),
    ]

    for name, icon, cat, freq_type, freq_count in default_habits:
        habit_repo.add_habit(name, icon, cat, freq_type, freq_count)


# ─── Splash Screen ────────────────────────────────────────────────────────────
def create_splash(app):
    """یه splash screen ساده هنگام لود برنامه نشون می‌ده."""
    splash = QSplashScreen()
    splash.setFixedSize(400, 220)
    splash.setStyleSheet("""
        QSplashScreen {
            background-color: #0f0f14;
            border: 1px solid rgba(124,92,191,0.4);
            border-radius: 16px;
        }
    """)

    # محتوای splash
    lbl = QLabel(splash)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.resize(400, 220)
    lbl.setText(
        "<div style='color:#f0eeff; font-family:Segoe UI;'>"
        "<div style='font-size:36px; margin-bottom:8px;'>✦</div>"
        "<div style='font-size:22px; font-weight:bold; color:#9b7de8;'>Smart Life Dashboard</div>"
        "<div style='font-size:13px; color:#888899; margin-top:8px;'>Loading your data...</div>"
        "</div>"
    )

    # وسط صفحه
    screen = app.primaryScreen().geometry()
    x = (screen.width()  - splash.width())  // 2
    y = (screen.height() - splash.height()) // 2
    splash.move(x, y)
    splash.show()
    app.processEvents()
    return splash


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Smart Life Dashboard")
    app.setApplicationVersion("1.0.0")

    # فونت پیش‌فرض
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # نمایش splash
    splash = create_splash(app)

    # ─ مقداردهی اولیه ─
    splash.showMessage("Initializing database...",
                       Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                       QColor("#888899"))
    app.processEvents()

    init_db()

    splash.showMessage("Loading your data...",
                       Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                       QColor("#888899"))
    app.processEvents()

    seed_data()

    # ─ ساخت پنجره اصلی ─
    splash.showMessage("Starting app...",
                       Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                       QColor("#888899"))
    app.processEvents()

    from ui.main_window import MainWindow
    window = MainWindow()

    # بستن splash و نمایش پنجره اصلی
    QTimer.singleShot(800, lambda: (splash.finish(window), window.show()))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()