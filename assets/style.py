from PyQt6.QtWidgets import QFrame



BG_MAIN = "#0f0f14"
BG_SIDEBAR = "#16161f"
BG_CARD = "#1e1e2a"
BG_CARD2 = "#252535"
ACCENT = "#7c5cbf"
ACCENT2 = "#9b7de8"
TEXT_PRIMARY = "#f0eeff"
TEXT_MUTED = "#888899"
GREEN = "#3ecf8e"
ORANGE = "#f59e42"
BLUE = "#4fa3e0"
RED = "#e05c5c"

GLOBAL_STYLE = f"""
QMainWindow {{
    background-color: {BG_MAIN};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', Arial, sans-serif;
}}
QMainWindow > QWidget {{
    background-color: {BG_MAIN};
    color: {TEXT_PRIMARY};
}}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {BG_CARD}; width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {ACCENT}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""

def make_card(parent=None, radius=14, color=BG_CARD):
    card = QFrame(parent)
    card.setStyleSheet(f"""
        QFrame {{
            background-color: {color};
            border-radius: {radius}px;
        }}
    """)
    return card
