import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()

        label = QLabel("Вы действительно хотите выйти?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        btn_yes = QPushButton("Да")
        btn_no = QPushButton("Нет")

        btn_yes.setMinimumHeight(40)
        btn_no.setMinimumHeight(40)

        btn_yes.clicked.connect(self.accept)
        btn_no.clicked.connect(self.reject)

        buttons_layout.addWidget(btn_yes)
        buttons_layout.addWidget(btn_no)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)



class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlappyBird")
        self.setFixedSize(400, 350)

        self.title = QLabel("FlappyBird")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.title.setFont(font)

        self.btn_play = QPushButton("Играть")
        self.btn_settings = QPushButton("Настройки")
        self.btn_exit = QPushButton("Выход")

        for btn in [self.btn_play, self.btn_settings, self.btn_exit]:
            btn.setMinimumHeight(50)
            btn.setFont(QFont("Arial", 12))

        self.btn_play.clicked.connect(self.on_play)
        self.btn_settings.clicked.connect(self.on_settings)
        self.btn_exit.clicked.connect(self.on_exit)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addSpacing(20)
        layout.addWidget(self.btn_play)
        layout.addSpacing(10)
        layout.addWidget(self.btn_settings)
        layout.addSpacing(10)
        layout.addWidget(self.btn_exit)
        layout.addStretch(1)

        self.setLayout(layout)

    def on_play(self):
        print("Запускаем игру...")

    def on_settings(self):
        print("Открываем настройки...")

    def on_exit(self):
        dialog = ConfirmationDialog(self)
        if dialog.exec():
            print("Выход из игры...")
            self.close()
        else:
            print("Отмена выхода")



def main():
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
