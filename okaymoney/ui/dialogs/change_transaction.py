from ...user_save_load import save
from .transaction_add import TransactionAddDialog
from ...util import INCOME


class TransactionChangeDialog(TransactionAddDialog):
    """Диалог изменения транзакции, наследованный от диалога добавления транзакции.

    *Файл интерфейса:* ``ui/dialogs/transaction_add.ui``
    """

    ui_path = 'ui/dialogs/transaction_add.ui'

    def __init__(self, user, transaction, account):
        super().__init__(user)

        self.user = user
        self.transaction = transaction
        self.account = account

        self.setWindowTitle("Изменить транзакцию")
        if self.transaction.type == INCOME:
            self.transaction_sum.setText(str(transaction.delta))
        else:
            self.transaction_sum.setText(str(-self.transaction.delta))
        self.income_radio.setChecked(self.transaction.type == INCOME)
        self.spend_radio.setChecked(self.transaction.type != INCOME)
        self.change_categories()
        self.note_text.setText(self.transaction.note)
        self.date.setDate(self.transaction.date)
        self.accounts_box.setCurrentIndex(self.user.accounts.index(self.account))
        self.categories_box.setCurrentIndex(
            self.user.income_categories.index(self.transaction.category)
            if self.transaction.type == INCOME else self.user.spend_categories.index(
                self.transaction.category))

    def add_transaction(self, tr, acc):
        self.account.remove_transaction(self.transaction, self.user.negative_balance_information)
        acc.add_transaction(tr, self.user.negative_balance_information)
        save(self.user, self)
        self.close()
