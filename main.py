import sys
from PyQt6.QtWidgets import QApplication
from ui.dashboard_window import DashboardWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DashboardWindow()
    window.show()

    sys.exit(app.exec())