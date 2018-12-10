from .ui_dialog import UIDialog
from datetime import datetime
from PyQt5.QtCore import QDate
from ...transaction import Transaction
from decimal import Decimal
from ..messagebox import error
from ...user_save_load import save


class TransactionAddDialog(UIDialog):
    """Диалог добавления новой транзакции.

    *Файл интерфейса:* ``ui/dialogs/transaction_add.ui``
    """

    ui_path = 'ui/dialogs/transaction_add.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.spend_radio.setChecked(True)
        self.categories_box.addItems(self.user.spend_categories)
        self.accounts_box.addItems([account.name for account in self.user.accounts])
        self.ok_btn.clicked.connect(self.add_transaction)
        self.cancel_btn.clicked.connect(self.close)
        self.date.setDate(QDate(datetime.now().year, datetime.now().month, datetime.now().day))

        self.spend_radio.clicked.connect(self.change_categories)
        self.income_radio.clicked.connect(self.change_categories)

    def change_categories(self):
        self.categories_box.clear()
        self.categories_box.addItems(self.user.spend_categories if self.spend_radio.isChecked()
                                     else self.user.income_categories)

    def add_transaction(self):
        try:
            transaction_sum = Decimal(self.transaction_sum.text())
            date = self.date.date()
            note = self.note_text.toPlainText()
            category = self.categories_box.currentText()
            account_name = self.accounts_box.currentText()
            if self.spend_radio.isChecked():
                transaction_sum *= -1 if transaction_sum > 0 else 1
                transaction = Transaction(category, transaction_sum, date, note)
            else:
                transaction_sum *= 1 if transaction_sum > 0 else -1
                transaction = Transaction(category, transaction_sum, date, note)
            account = [account for account in self.user.accounts if account.name == account_name][0]
            account.add_transaction(transaction)
            save(self.user, self)
            self.close()
        except Exception:
            error('Ошибка, попробуйте еще раз.', self)
