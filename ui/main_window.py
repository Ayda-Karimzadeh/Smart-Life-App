from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)
from repositories.task_repository import TaskRepository
from ui.Widgets.task_card import TaskCard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Life App")
        self.setMinimumSize(400, 300)

        self.repo = TaskRepository()
        self.editing_task_id = None

        self._setup_ui()

        self.load_tasks()

    def _setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Smart Life App")
        layout.addWidget(title)

        subtitle = QLabel("Today's Tasks")
        layout.addWidget(subtitle)

        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout()
        self.tasks_container.setLayout(self.tasks_layout)

        layout.addWidget(self.tasks_container)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.save_task)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_task(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            return

        if self.editing_task_id is not None:
            self.repo.update_task(self.editing_task_id, task_text)
            self._clear_edit_mode()
        else:
            self.repo.add_task(task_text)
            self.task_input.clear()

        self.load_tasks()

    def delete_task(self, task_id):
        if self.editing_task_id == task_id:
            self._clear_edit_mode()
        self.repo.delete_task(task_id)
        self.load_tasks()

    def edit_task(self, task_id, title):
        self.editing_task_id = task_id
        self.task_input.setText(title)
        self.task_input.setFocus()
        self.add_button.setText("Update Task")

    def _clear_edit_mode(self):
        self.editing_task_id = None
        self.task_input.clear()
        self.add_button.setText("Add Task")

    def load_tasks(self):
        self.clear_layout(self.tasks_layout)

        tasks = self.repo.get_all_tasks()

        for task in tasks:
            task_id, title, is_done = task

            card = TaskCard(task_id, title, is_done)

            card.delete_requested.connect(self.delete_task)
            card.edit_requested.connect(self.edit_task)
            card.toggle_requested.connect(self.toggle_task)

            self.tasks_layout.addWidget(card)

    def toggle_task(self, task_id, is_done):
        self.repo.toggle_task(task_id, is_done)
        self.load_tasks()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()