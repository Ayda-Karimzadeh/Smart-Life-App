from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
)


class DashboardWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Life Dashboard")
        self.resize(1400, 900)

        self.setStyleSheet("""
            QMainWindow{
                background:#070B17;
            }

            QLabel{
                color:white;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        sidebar = self.create_sidebar()
        content = self.create_content()

        root.addWidget(sidebar)
        root.addWidget(content, 1)

    def create_sidebar(self):

        frame = QFrame()
        frame.setFixedWidth(250)

        frame.setStyleSheet("""
            background:#0F1324;
            border-right:1px solid #1D2235;
        """)

        layout = QVBoxLayout(frame)

        title = QLabel("Smart Life")
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:20px;
        """)

        layout.addWidget(title)

        pages = [
            "Dashboard",
            "Habits",
            "Goals",
            "Tasks",
            "Time Tracking",
            "Analytics",
        ]

        for page in pages:

            btn = QPushButton(page)

            btn.setStyleSheet("""
                QPushButton{
                    color:white;
                    text-align:left;
                    padding:15px;
                    border:none;
                    border-radius:12px;
                    background:#1A2040;
                }

                QPushButton:hover{
                    background:#2A3160;
                }
            """)

            layout.addWidget(btn)

        layout.addStretch()

        return frame

    def create_content(self):

        container = QWidget()

        layout = QVBoxLayout(container)

        hero = QFrame()

        hero.setStyleSheet("""
            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:1,
                stop:0 #1B2A52,
                stop:1 #41205E
            );
            border-radius:25px;
        """)

        hero_layout = QVBoxLayout(hero)

        title = QLabel("Good evening, Ayda! ☀️")
        title.setStyleSheet("""
            font-size:36px;
            font-weight:700;
        """)

        subtitle = QLabel(
            "You're doing amazing! Keep pushing forward."
        )

        subtitle.setStyleSheet("""
            color:#C7CAE0;
            font-size:18px;
        """)

        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)

        layout.addWidget(hero)

        row = QHBoxLayout()

        cards = [
            ("92%", "Daily Progress"),
            ("3/4", "Habits"),
            ("3", "Goals"),
            ("4.5h", "Focus Time"),
        ]

        for value, text in cards:

            card = QFrame()

            card.setMinimumHeight(180)

            card.setStyleSheet("""
                background:#101526;
                border:1px solid #232A40;
                border-radius:20px;
            """)

            card_layout = QVBoxLayout(card)

            value_lbl = QLabel(value)

            value_lbl.setStyleSheet("""
                font-size:34px;
                font-weight:bold;
            """)

            text_lbl = QLabel(text)

            text_lbl.setStyleSheet("""
                color:#A6ABBF;
                font-size:16px;
            """)

            card_layout.addStretch()
            card_layout.addWidget(value_lbl)
            card_layout.addWidget(text_lbl)

            row.addWidget(card)

        layout.addLayout(row)

        return container
