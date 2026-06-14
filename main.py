import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db_manager import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())