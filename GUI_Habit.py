import sys
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QTimer
from Habit import (
    load_data,
    save_data,
    add_habit,
    list_habits,
    done_habit,
    remove_habit,
    stats_habit,
    rename_habit,
)


class Habit(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 200, 50)
        self.setWindowTitle("Трекер привычек")

        self.data = load_data()

        self.label = QLabel("Выберите функцию")
        self.label.resize(self.label.sizeHint())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_habit = QPushButton("ADD", self)
        self.add_habit.resize(self.add_habit.sizeHint())
        self.add_habit.clicked.connect(self.window_add_habit)

        self.done_habit = QPushButton("DONE", self)
        self.done_habit.resize(self.done_habit.sizeHint())
        self.done_habit.clicked.connect(self.window_done_habit)

        self.remove_habit = QPushButton("REMOVE", self)
        self.remove_habit.resize(self.remove_habit.sizeHint())
        self.remove_habit.clicked.connect(self.window_remove_habit)

        self.show_stats = QPushButton("SHOW STATS", self)
        self.show_stats.resize(self.show_stats.sizeHint())
        self.show_stats.clicked.connect(self.window_show_stats_habit)

        self.rename = QPushButton("RENAME HABIT", self)
        self.rename.resize(self.rename.sizeHint())
        self.rename.clicked.connect(self.window_rename_habit)

        self.habit_list = QPushButton("LIST HABITS", self)
        self.habit_list.resize(self.habit_list.sizeHint())
        self.habit_list.clicked.connect(self.window_show_list)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.add_habit, 1, 0)
        self.grid.addWidget(self.done_habit, 2, 0)
        self.grid.addWidget(self.show_stats, 3, 0)
        self.grid.addWidget(self.remove_habit, 4, 0)
        self.grid.addWidget(self.rename, 5, 0)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.vbox.addWidget(self.habit_list)
        self.vbox.addStretch()

        self.setLayout(self.vbox)

    def window_add_habit(self):
        self.hide()
        self.window_add = AddHabit(self, self.data)
        self.window_add.show()

    def window_show_list(self):
        self.hide()
        self.window_list = ListHabit(self, self.data)
        self.window_list.show()

    def window_done_habit(self):
        self.hide()
        self.window_done_habit = DoneHabit(self, self.data)
        self.window_done_habit.show()

    def window_remove_habit(self):
        self.hide()
        self.window_remove_habit = RemoveHabit(self, self.data)
        self.window_remove_habit.show()

    def window_show_stats_habit(self):
        self.hide()
        self.window_show_stats_habit = Stat(self, self.data)
        self.window_show_stats_habit.show()

    def window_rename_habit(self):
        self.hide()
        self.window_rename_habit = RenameHabit(self, self.data)
        self.window_rename_habit.show()


class AddHabit(QWidget):
    def __init__(self, main_window, data):
        super().__init__()
        self.data = data
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 200, 50)
        self.setWindowTitle("Добавить привычку")

        self.label = QLabel("Введите название привычки, которую хотите добавить:")
        self.label.resize(self.label.sizeHint())

        self.line = QLineEdit()
        self.line.resize(self.line.sizeHint())

        self.add = QPushButton("ADD")
        self.add.setFixedSize(50, 25)
        self.add.clicked.connect(self.wadd_habit)

        self.habit_list = QLabel("")

        self.back = QPushButton("Назад")
        self.back.setFixedSize(50, 25)
        self.back.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line)
        self.vbox.addWidget(self.add)
        self.vbox.addWidget(self.back)
        self.vbox.addWidget(self.habit_list)

        self.setLayout(self.vbox)

        self.refresh_list()

    def wadd_habit(self):
        data = add_habit(self.data, self.line.text())
        if isinstance(data, dict):
            self.data = data
            save_data(self.data)
            self.refresh_list()
            self.line.setText("Привычка успешно добавлена")
            QTimer.singleShot(1000, self.line.clear)
        else:
            self.line.setText(data)

    def refresh_list(self):
        lst = []
        update_list = list_habits(self.data)
        for id_h, habit in update_list.items():
            lst.append(f"{id_h}. {habit}")
        self.habit_list.setText("\n".join(lst))
        self.adjustSize()


class ListHabit(QWidget):
    def __init__(self, main_window, data):
        super().__init__()
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 300, 50)
        self.setWindowTitle("Окно списка привычек")

        self.label = QLabel("Список привычек")
        self.label.resize(self.label.sizeHint())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_list = show_list(self.data)

        self.back = QPushButton("Назад")
        self.back.resize(self.back.sizeHint())
        self.back.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label_list)
        self.vbox.addWidget(self.back)
        self.vbox.addStretch()

        self.setLayout(self.vbox)


class DoneHabit(QWidget):
    def __init__(self, main_window, data):
        self.main_window = main_window
        self.data = data
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 50)
        self.setWindowTitle("Отметка привычки")

        self.label = QLabel("Напишите привычку, которую хотите отметить:")
        self.label.resize(self.label.sizeHint())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line = QLineEdit()
        self.line.resize(self.line.sizeHint())

        self.done = QPushButton("Отметить", self)
        self.done.resize(self.done.sizeHint())
        self.done.clicked.connect(lambda: self.wdone_habit(self.data, self.line.text()))

        self.habit_list = show_list(self.data)

        self.back = QPushButton("Назад", self)
        self.back.resize(self.back.sizeHint())
        self.back.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.grid = QGridLayout()
        self.grid.addWidget(self.done, 0, 0)
        self.grid.addWidget(self.back, 0, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line)
        self.vbox.addLayout(self.grid)
        self.vbox.addWidget(self.habit_list)
        self.vbox.addStretch()

        self.setLayout(self.vbox)

    def wdone_habit(self, data, habit_name):
        data = done_habit(data, habit_name)
        if isinstance(data, dict):
            self.data = data
            save_data(self.data)
            self.line.setText("Привычка отмечена")
            QTimer.singleShot(1000, self.line.clear)
        else:
            self.line.setText(data)
            QTimer.singleShot(1000, self.line.clear)


class RemoveHabit(QWidget):

    def __init__(self, main_window, data):
        super().__init__()
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle("Удалить привычку")

        self.label = QLabel("Напишите привычку, которую хотите удалить:")
        self.label.resize(self.label.sizeHint())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line = QLineEdit()
        self.line.resize(self.line.sizeHint())

        self.remove = QPushButton("Удалить", self)
        self.remove.resize(self.remove.sizeHint())
        self.remove.clicked.connect(
            lambda: self.wremove_habit(self.data, self.line.text())
        )

        self.habit_list = QLabel("")

        self.back = QPushButton("Назад", self)
        self.back.resize(self.back.sizeHint())
        self.back.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.grid = QGridLayout()
        self.grid.addWidget(self.remove, 0, 0)
        self.grid.addWidget(self.back, 0, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line)
        self.vbox.addLayout(self.grid)
        self.vbox.addWidget(self.habit_list)

        self.setLayout(self.vbox)

        self.refresh_list()

    def wremove_habit(self, data, habit_name):
        data = remove_habit(data, habit_name)
        if isinstance(data[1], dict):
            self.data = data[1]
            save_data(self.data)
            self.refresh_list()
            self.line.setText(data[0])
            QTimer.singleShot(1000, self.line.clear)
        else:
            self.line.setText(data)
            QTimer.singleShot(1000, self.line.clear)

    def refresh_list(self):
        lst = []
        update_list = list_habits(self.data)
        for id_h, habit in update_list.items():
            lst.append(f"{id_h}. {habit}")
        self.habit_list.setText("\n".join(lst))
        self.adjustSize()


class Stat(QWidget):

    def __init__(self, main_window, data):
        self.main_window = main_window
        self.data = data
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle("Список привычек")

        self.label = QLabel("Выберите привычку, статистику которой хотите посмотреть:")
        self.label.resize(self.label.sizeHint())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if hasattr(self, "vbox"):
            self.clear_layout(self.vbox)
        else:
            self.vbox = QVBoxLayout()

        self.label_list = self.mshow_list()

        self.back_main = QPushButton("Назад")
        self.back_main.resize(self.back_main.sizeHint())
        self.back_main.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.vbox.addWidget(self.label_list)
        self.vbox.addWidget(self.back_main)

        if self.layout() is None:
            self.setLayout(self.vbox)

        self.adjustSize()

    def show_stat(self, data, name):
        self.clear_layout(self.vbox)
        stats = stats_habit(data, name)
        if not isinstance(stats, str):
            stats = f"Статистика для привычки '{name}' пока не доступна"
        self.stat_label = QLabel(stats)
        self.space = QLabel(" ")

        self.back = QPushButton("Назад", self)
        self.back.clicked.connect(self.initUI)

        self.vbox.addWidget(self.stat_label)
        self.vbox.addWidget(self.space)
        self.vbox.addWidget(self.back)
        self.vbox.addStretch()

    def mshow_list(self):
        listHabits = list_habits(self.data)
        container = QWidget()
        layout = QVBoxLayout(container)
        if listHabits:
            for id_h, habit in listHabits.items():
                btn = QPushButton(f"{id_h}. {habit}")
                btn.clicked.connect(
                    lambda checked, name=habit: self.show_stat(self.data, name)
                )
                layout.addWidget(btn)
            return container
        else:
            btn = QPushButton("Список пуст (Нажмите, чтобы закрыть)")
            btn.clicked.connect(self.close_and_return)
            layout.addWidget(btn)
            return container

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())


class RenameHabit(QWidget):

    def __init__(self, main_window, data):
        super().__init__()
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle("Переименование привычки")

        if hasattr(self, "vbox"):
            self.clear_layout(self.vbox)
        else:
            self.vbox = QVBoxLayout()

        self.label = QLabel(
            "Дайте новое название для любой привычки,\nа затем выберите привычку, которую хотите переименовать:",
            self,
        )
        self.label.resize(self.label.sizeHint())

        self.line = QLineEdit()
        self.line.resize(self.line.sizeHint())

        self.label_list = self.mshow_list()

        self.space = QLabel(" ")

        self.back = QPushButton("Назад", self)
        self.back.resize(self.back.sizeHint())
        self.back.clicked.connect(lambda: close_and_return(self, self.main_window))

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line)
        self.vbox.addWidget(self.space)
        self.vbox.addWidget(self.label_list)
        self.vbox.addWidget(self.space)
        self.vbox.addWidget(self.back)

        if self.layout() is None:
            self.setLayout(self.vbox)

        self.adjustSize()

    def mshow_list(self):
        listHabits = list_habits(self.data)
        container = QWidget()
        layout = QVBoxLayout(container)
        if listHabits:
            for id_h, habit in listHabits.items():
                btn = QPushButton(f"{id_h}. {habit}")
                btn.clicked.connect(
                    lambda checked, name=habit: self.procces_name(
                        name, self.line.text()
                    )
                )
                layout.addWidget(btn)
            return container
        else:
            btn = QPushButton("Список пуст (Нажмите, чтобы закрыть)")
            btn.clicked.connect(lambda: close_and_return(self, self.main_window))
            layout.addWidget(btn)
            return container

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def procces_name(self, name, new_name):
        if not new_name.strip():
            self.line.setPlaceholderText("Сначала введите новое название здесь!")
            return
        self.line.setText(str(rename_habit(self.data, name, new_name)))
        self.initUI()
        QTimer.singleShot(1000, self.line.clear)


def close_and_return(this_window, main_window):
    main_window.show()
    this_window.close()


def show_list(data):
    listHabits = list_habits(data)
    text_lines = []
    for id_h, habit in listHabits.items():
        text_lines.append(f"{id_h}. {habit}")
    final_text = "\n".join(text_lines)

    return QLabel(final_text if final_text else "Список пуст")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    habit = Habit()
    habit.show()
    sys.exit(app.exec())
