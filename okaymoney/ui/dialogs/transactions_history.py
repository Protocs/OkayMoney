from .ui_dialog import UIDialog
from ...util import INCOME, MONTHS
from .change_transaction import TransactionChangeDialog
from ...user_save_load import save


class TransactionsHistoryDialog(UIDialog):
    """Диалог истории транзакций.

    *Файл интерфейса:* ``ui/dialogs/transactions_history.ui``
    """

    ui_path = "ui/dialogs/transactions_history.ui"

    def __init__(self, user, main_window):
        super().__init__()

        self.user = user
        self.main_window = main_window

        self.account = None
        self.accounts_box.addItems([account.name for account in self.user.accounts])
        self.accounts_box.currentIndexChanged.connect(self.change_transactions)
        self.history_transactions.itemClicked.connect(self.show_details)
        self.transactions = []

        self.change_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.change_btn.clicked.connect(self.show_transaction_change_dialog)
        self.delete_btn.clicked.connect(self.delete_transaction)

        self.yearSelect.currentIndexChanged.connect(self.change_current_year)
        self.monthSelect.currentIndexChanged.connect(self.change_current_month)
        self.daySelect.currentIndexChanged.connect(self.change_current_day)
        self.current_year = None
        self.current_month = None
        self.current_day = None

        if self.user.accounts:
            self.change_transactions()

    def change_transactions(self):
        old_account_name = self.account.name if self.account else None
        self.account = [
            acc
            for acc in self.user.accounts
            if acc.name == self.accounts_box.currentText()
        ][0]
        self.transactions = []
        for tr in self.account.transactions:
            date = tr.date.date()
            if self.current_year is not None and date.year() != self.current_year:
                continue
            if self.current_month is not None and date.month() != self.current_month:
                continue
            if self.current_day is not None and date.day() != self.current_day:
                continue
            self.transactions.append(tr)

        self.history_transactions.clear()
        for transaction in self.transactions:
            self.history_transactions.addItem(
                "{}{}\t{}".format(
                    "+" if transaction.type == INCOME else "",
                    str(transaction.delta),
                    transaction.date.toString("ddd dd MMM yyyy"),
                )
            )
        self.change_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.details.setText("")

        # Меняем комбобоксы с выбором даты только в том случае, если была смена счёта
        if self.accounts_box.currentText() != old_account_name:
            self.fill_date_selectors()

    def show_details(self):
        self.change_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

        transaction = self.transactions[self.history_transactions.currentRow()]
        self.details.setText(
            "Категория:\n{}".format(transaction.category)
            + ("\n\nОписание:\n{}".format(transaction.note) if transaction.note else "")
        )

    def delete_transaction(self):
        transaction = self.transactions[self.history_transactions.currentRow()]
        # month, year = transaction.date.date().month(), transaction.date.date().year()
        if self.account.remove_transaction(
                transaction, self.user.negative_balance_information
        ):
            self.change_transactions()
            save(self.user, self)
            # self.main_window.pie_chart.upd(month, year)
            self.main_window._update_monthly()
            self.main_window.fill_accounts()

    def show_transaction_change_dialog(self):
        transaction = self.transactions[self.history_transactions.currentRow()]
        # month, year = transaction.date.date().month(), transaction.date.date().year()
        self.transactions_change_dialog = TransactionChangeDialog(
            self.user, transaction, self.account
        )
        self.transactions_change_dialog.exec()
        self.change_transactions()
        # self.main_window.pie_chart.upd(month, year)
        self.main_window._update_monthly()
        self.main_window.fill_accounts()

    def fill_date_selectors(self):
        for select in [self.yearSelect, self.monthSelect, self.daySelect]:
            select.clear()
            select.addItem("Все")

        years, months, days = [], [], []
        for tr in self.transactions:
            date = tr.date.date()
            year = date.year()
            month = date.month()
            day = date.day()
            if year not in years:
                years.append(year)
                self.yearSelect.addItem(str(year))
            if month not in months:
                months.append(month)
                self.monthSelect.addItem(MONTHS[month - 1])
            if day not in days:
                days.append(day)
                self.daySelect.addItem(str(day))

    def change_current_year(self):
        current = self.yearSelect.currentText()
        if current:
            self.current_year = None if current == "Все" else int(current)
            self.change_transactions()

    def change_current_month(self):
        current = self.monthSelect.currentText()
        if current:
            self.current_month = None if current == "Все" else MONTHS.index(current) + 1
            self.change_transactions()

    def change_current_day(self):
        current = self.daySelect.currentText()
        if current:
            self.current_day = None if current == "Все" else int(current)
            self.change_transactions()
