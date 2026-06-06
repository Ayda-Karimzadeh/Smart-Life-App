from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

class TaskCard(QWidget):
    delete_requested = pyqtSignal(int)
    toggle_requested = pyqtSignal(int, bool)
    edit_requested = pyqtSignal(int, str)

    def __init__(self, task_id, title, is_done=False):
        super().__init__()
        self.task_id = task_id
        self.title = title
        self.is_done = is_done

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(bool(self.is_done))

        self.label = QLabel(self.title)

        top_layout.addWidget(self.checkbox)
        top_layout.addWidget(self.label)

        bottom_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        bottom_layout.addWidget(self.edit_btn)
        bottom_layout.addWidget(self.delete_btn)

        self.layout.addLayout(top_layout)
        self.layout.addLayout(bottom_layout)

        self.setLayout(self.layout)

    def connect_signals(self):
        self.delete_btn.clicked.connect(self.on_delete)
        self.edit_btn.clicked.connect(self.on_edit)
        self.checkbox.stateChanged.connect(self.on_toggle)

    def on_delete(self):
        self.delete_requested.emit(self.task_id)

    def on_edit(self):
        self.edit_requested.emit(self.task_id, self.title)

    def on_toggle(self):
        self.toggle_requested.emit(
            self.task_id,
            self.checkbox.isChecked()
        )