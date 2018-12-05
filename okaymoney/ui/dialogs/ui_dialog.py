from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class UIDialog(QDialog):
    """
    Класс диалога, который автоматически подгружает UI из файла по пути,
    содержащемся в переменной класса ``ui_path``.

    Пример::

        class TransactionAddDialog(UIDialog):
            ui_path = 'ui/login.ui'
            ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(self.ui_path, self)
