from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QLineEdit
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Life App")
        self.setMinimumSize(400, 300)

        self._setup_ui()

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
            self.tasks_list.addItem(task_text)
            self.task_input.clear()

    def delete_task(self):
        selected_item = self.tasks_list.currentItem()

        if selected_item:
            self.tasks_list.takeItem(self.tasks_list.row(selected_item))

    def edit_task(self):
        selected_item = self.tasks_list.currentItem()

        if selected_item:
            new_text = self.task_input.text()

            if new_text:
                selected_item.setText(new_text)
                self.task_input.clear()