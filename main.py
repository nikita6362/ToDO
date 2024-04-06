from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QColorDialog, QDateEdit, QLabel, QCheckBox, QListWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QListWidget, QMessageBox
from PyQt5.QtGui import QFont, QColor
import os, json

font = QFont()
font.setFamily("Montserrat")
font.setPointSize(10)

class AddCategoryDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить категорию")
        self.setFixedSize(300, 150)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Название категории:")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.color_label = QLabel("Цвет категории:")
        self.layout.addWidget(self.color_label)

        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.clicked.connect(self.choose_color)
        self.layout.addWidget(self.color_button)

        self.color = None

        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

class MainWin(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.set_appear()
        self.connects()

        self.show()

    def initUI(self):
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите задачу...")
        self.task_but_add = QPushButton('Добавить')

        self.task_field = QListWidget()

        self.task_but_del = QPushButton('Удалить выбранную задачу')
        self.category_but_add = QPushButton("Добавить категорию")

        self.task_status = QLabel('')

        self.category_input = QComboBox()
        self.category_input.addItem('Общее')
        self.category_input.addItem("Работа")
        self.category_input.addItem("Дом")
        self.category_input.addItem("Учеба")
        self.add_date = QDateEdit()
        self.add_date.setDate(QDate.currentDate())
        self.add_date.setCalendarPopup(True)
        self.date_lable = QLabel('Выполнить до:')

        self.line_main = QVBoxLayout()
        self.line_hor = QHBoxLayout()
        self.line_hor2 = QHBoxLayout()

        self.task_input.setFont(QFont("Montserrat", 8))
        self.category_input.setFont(QFont("Montserrat", 8))

        self.line_hor.addWidget(self.task_input)
        self.line_hor.addWidget(self.category_input)
        self.line_hor.addWidget(self.task_but_add)

        self.line_hor2.addWidget(self.date_lable)
        self.line_hor2.addWidget(self.add_date)
        
        self.line_main.addLayout(self.line_hor)
        self.line_main.addLayout(self.line_hor2)
        self.line_main.addWidget(self.category_but_add)       
        
        self.line_main.addWidget(self.task_field)
        self.line_main.addWidget(self.task_but_del)

        self.line_main.addWidget(self.task_status)

        self.setLayout(self.line_main)

        self.categories = {"Общее": QColor('lightGray'), "Работа": QColor('lightBlue'), "Дом": QColor('lightGreen'), "Учеба": QColor('lightYellow')}
        
        self.load_tasks()

    def add_task(self):
        task_text = self.task_input.text()
        category = self.category_input.currentText()
        date = self.add_date.date().toString("dd.MM.yyyy")

        if task_text:
            item = QListWidgetItem(f"{category}: {task_text} (до {date})")
            self.task_field.addItem(item)
            
            if category in self.categories:
                item.setBackground(self.categories[category])

            self.task_input.clear()
            self.task_status.setText("Задача добавлена успешно.")
            self.save_tasks()
        
        else:
            QMessageBox.warning(self, 'Пустое поле', 'Пожалуйста, введите текст задачи!')
    
    def del_task(self):
        selected_item = self.task_field.currentItem()
        if selected_item:
            self.task_field.takeItem(self.task_field.row(selected_item))
            self.task_status.setText('Задача удалена!')
            self.save_tasks()
        else:
            QMessageBox.warning(self, 'Нет выбранной задачи', 'Пожалуйста, выберите задачу!')

    def add_category(self):
        dialog = AddCategoryDialog()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_input.text()
            color = dialog.color
            if name and color:
                self.category_input.addItem(name)
                self.categories[name] = color
                self.task_status.setText(f"Категория '{name}' добавлена")
                self.save_tasks()

    def connects(self):
        self.task_but_add.clicked.connect(self.add_task)
        self.task_but_del.clicked.connect(self.del_task)
        self.category_but_add.clicked.connect(self.add_category)

    def set_appear(self):
        self.setWindowTitle('ToDo - список дел')
        self.resize(600, 500)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                for task in data:
                    item = QListWidgetItem(task["text"])
                    category = task["category"]
                    deadline = QDate.fromString(task["deadline"], "dd.MM.yyyy")
                    self.task_field.addItem(item)
                    if category in self.categories:
                        item.setBackground(self.categories[category])
                    if "background_color" in task:
                        background_color = QColor(*task["background_color"])
                        item.setBackground(background_color)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        tasks = []
        for i in range(self.task_field.count()):
            item = self.task_field.item(i)
            text = item.text()
            category = self.category_input.currentText()
            deadline = self.add_date.date().toString("dd.MM.yyyy")
            tasks.append({
                "text": text,
                "category": category,
                "deadline": deadline,
                "background_color": item.background().color().getRgb()[:3]  
            })
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

app = QApplication([])
main_win = MainWin()
app.setFont(font)
app.exec_()