from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QLineEdit, QListWidgetItem
)
from repositories.task_repository import TaskRepository
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Life App")
        self.setMinimumSize(400, 300)

        self.repo = TaskRepository()

        self._setup_ui()

        self.tasks_list.itemChanged.connect(self.on_item_changed)

        self.load_tasks()

    def _setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Smart Life App")
        layout.addWidget(title)

        subtitle = QLabel("Today's Tasks")
        layout.addWidget(subtitle)

        self.tasks_list = QListWidget()
        layout.addWidget(self.tasks_list)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.tasks_list.addItem("Study PyQt6")
        self.tasks_list.addItem("Exercise")
        self.tasks_list.addItem("Read Book")

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Delete Task")
        layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_task)

        self.edit_button = QPushButton("Edit Task")
        layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.edit_task)

    def add_task(self):
        task_text = self.task_input.text()

        if task_text:
            self.repo.add_task(task_text)
            self.task_input.clear()
            self.load_tasks()

    def delete_task(self):
        selected_item = self.tasks_list.currentItem()

        if selected_item:
            task_id = selected_item.data(Qt.ItemDataRole.UserRole)

            self.repo.delete_task(task_id)
            self.load_tasks()

    def edit_task(self):
        selected_item = self.tasks_list.currentItem()

        if selected_item:
            new_text = self.task_input.text()

            if new_text:
                task_id = selected_item.data(Qt.ItemDataRole.UserRole)

                self.repo.update_task(task_id, new_text)

                self.task_input.clear()
                self.load_tasks()

    def load_tasks(self):
        self.tasks_list.blockSignals(True)

        self.tasks_list.clear()

        tasks = self.repo.get_all_tasks()

        for task in tasks:
            task_id = task[0]
            title = task[1]
            is_done = task[2]

            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, task_id)

            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            if is_done:
                item.setData(Qt.CheckState.Checked)
            else:
                item.setData(Qt.CheckState.Unchecked)

            self.tasks_list.addItem(item)

        self.tasks_list.blockSignals(False)

    def on_item_changed(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)

        if item.checkState() == Qt.CheckState.Checked:
            self.repo.toggle_task(task_id, 1)
        else:
            self.repo.toggle_task(task_id, 0)