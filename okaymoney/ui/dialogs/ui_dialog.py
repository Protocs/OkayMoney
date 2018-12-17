from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from okaymoney.util import find_data_file


class UIDialog(QDialog):
    """
    Класс диалога, который автоматически подгружает UI из файла по пути,
    содержащемся в переменной класса ``ui_path``.

    Пример::

        class TransactionAddDialog(UIDialog):
            ui_path = 'ui/transaction_add.ui'
            ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(find_data_file(self.ui_path), self)
