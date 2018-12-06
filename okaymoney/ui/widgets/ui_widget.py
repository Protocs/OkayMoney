from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt


class UIWidget(QWidget):
    """
    Класс виджета, который автоматически подгружает UI из файла по пути,
    содержащемся в переменной класса ``ui_path``.

    Пример::

        class UserLoginButton(UIWidget):
            ui_path = 'ui/login.ui'
            ...
    """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        uic.loadUi(self.ui_path, self)
