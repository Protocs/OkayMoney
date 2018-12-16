from datetime import datetime
from decimal import Decimal

from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon

from .ui_dialog import UIDialog
from ...transaction import Transaction
from ..messagebox import error
from ...user_save_load import save
from ...util import SPEND, SPEND_ICONS, INCOME_ICONS


class TransactionAddDialog(UIDialog):
    """Диалог добавления новой транзакции.

    *Файл интерфейса:* ``ui/dialogs/transaction_add.ui``
    """

    ui_path = 'ui/dialogs/transaction_add.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.spend_radio.setChecked(True)

        self.accounts_box.addItems([account.name for account in self.user.accounts])
        self.change_categories()

        self.date.setDate(QDate(datetime.now().year, datetime.now().month, datetime.now().day))

        self.ok_btn.clicked.connect(self.get_transaction)
        self.cancel_btn.clicked.connect(self.close)

        self.spend_radio.clicked.connect(self.change_categories)
        self.income_radio.clicked.connect(self.change_categories)

    def change_categories(self):
        self.categories_box.clear()
        categories = self.user.spend_categories if self.spend_radio.isChecked() \
            else self.user.income_categories
        icons = SPEND_ICONS if self.spend_radio.isChecked() else INCOME_ICONS
        for i in range(len(categories)):
            self.categories_box.addItem(categories[i])
            self.categories_box.setItemIcon(i, QIcon(icons[categories[i]]))

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
        except Exception:
            error('Ошибка, попробуйте еще раз.', self)

    def add_transaction(self, tr, acc):
        if len(str(tr.delta + acc.money)[1:] if tr.type == SPEND else str(
                tr.delta + acc.money)) > 15:
            error("Баланс на вашем счету не должен содержать в себе более 15 цифр.", self)
            return
        if acc.add_transaction(tr, self.user.negative_balance_information):
            save(self.user, self)
            self.close()
