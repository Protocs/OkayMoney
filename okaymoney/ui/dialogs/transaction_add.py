from datetime import datetime
from decimal import Decimal

from PyQt5.QtCore import QDate, QDateTime, QTime

from .ui_dialog import UIDialog
from ...transaction import Transaction
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

        self.date.setDate(QDate(datetime.now().year, datetime.now().month, datetime.now().day))

        self.ok_btn.clicked.connect(self.get_transaction)
        self.cancel_btn.clicked.connect(self.close)

        self.spend_radio.clicked.connect(self.change_categories)
        self.income_radio.clicked.connect(self.change_categories)

    def change_categories(self):
        self.categories_box.clear()
        self.categories_box.addItems(self.user.spend_categories if self.spend_radio.isChecked()
                                     else self.user.income_categories)

    def get_transaction(self):
        try:
            transaction_sum = Decimal(self.transaction_sum.text())
            date = self.date.date()
            note = self.note_text.toPlainText()
            category = self.categories_box.currentText()
            account_name = self.accounts_box.currentText()

            transaction_sum = -abs(transaction_sum) if self.spend_radio.isChecked() else abs(
                transaction_sum)
            now = datetime.now()
            transaction = Transaction(category, transaction_sum,
                                      QDateTime(date, QTime(now.hour, now.minute, now.second)), note)

            account = [acc for acc in self.user.accounts if acc.name == account_name][0]
            self.add_transaction(transaction, account)
        except Exception as e:
            print(e)
            error('Ошибка, попробуйте еще раз.', self)

    def add_transaction(self, tr, acc):
        try:
            acc.add_transaction(tr, self.user.negative_balance_information)
            save(self.user, self)
            self.close()
        except Exception as e:
            print(e)