from .ui_dialog import UIDialog
from ...util import INCOME
from .change_transaction import TransactionChangeDialog
from ...user_save_load import save


class TransactionsHistoryDialog(UIDialog):
    """Диалог истории транзакций.

    *Файл интерфейса:* ``ui/dialogs/transactions_history.ui``
    """

    ui_path = 'ui/dialogs/transactions_history.ui'

    def __init__(self, user, main_window):
        super().__init__()

        self.user = user
        self.main_window = main_window

        self.accounts_box.addItems([account.name for account in self.user.accounts])
        self.accounts_box.currentIndexChanged.connect(self.change_transactions)
        self.history_transactions.itemClicked.connect(self.show_details)

        self.change_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.change_btn.clicked.connect(self.show_transaction_change_dialog)
        self.delete_btn.clicked.connect(self.delete_transaction)

        if self.user.accounts:
            self.change_transactions()

    def change_transactions(self):
        self.account = \
            [acc for acc in self.user.accounts if acc.name == self.accounts_box.currentText()][0]
        self.transactions = [acc.transactions for acc in self.user.accounts
                             if self.account.name == acc.name][0]
        self.history_transactions.clear()
        for transaction in self.transactions:
            self.history_transactions.addItem(
                "{}{}\t{}".format('+' if transaction.type == INCOME else '', str(transaction.delta),
                                  transaction.date.toString("ddd dd MMM yyyy")))
        self.change_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.details.setText("")

    def show_details(self):
        self.change_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

        transaction = self.transactions[self.history_transactions.currentRow()]
        self.details.setText(
            "Категория:\n{}".format(transaction.category)
            + ("\n\nОписание:\n{}".format(transaction.note) if transaction.note else ""))

    def delete_transaction(self):
        if self.account.remove_transaction(self.transactions[self.history_transactions.currentRow()],
                                           self.user.negative_balance_information):
            self.change_transactions()
            save(self.user, self)
            self.main_window.pie_chart.upd()
            self.main_window._update_monthly()
            self.main_window.fill_accounts()

    def show_transaction_change_dialog(self):
        self.transactions_change_dialog = \
            TransactionChangeDialog(self.user,
                                    self.transactions[self.history_transactions.currentRow()],
                                    self.account)
        self.transactions_change_dialog.exec()
        self.change_transactions()
        self.main_window.pie_chart.upd()
        self.main_window._update_monthly()
        self.main_window.fill_accounts()
