from ..util import INCOME, SPEND
from .ui_window import UIWindow
from .widgets.pie_chart import PieChart
from .dialogs.new_account import NewAccountDialog
from .dialogs.accounts_filter import AccountsFilterDialog
from .dialogs.transaction_add import TransactionAddDialog
from .dialogs.transactions_history import TransactionsHistoryDialog


class MainWindow(UIWindow):
    """Основное окно приложения.

    *Файл интерфейса:* ``ui/main.ui``
    """

    ui_path = 'ui/main.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.add_account_btn.clicked.connect(self.show_add_account_dialog)
        self.accounts_filter_btn.clicked.connect(self.show_accounts_filter_dialog)
        self.new_transaction_btn.clicked.connect(self.show_add_transaction_dialog)
        self.transactions_history_btn.clicked.connect(self.show_transactions_history_dialog)

        self.pie_chart = PieChart(self.pie_place, self.user)

        self.OnlyIncomes.clicked.connect(self.show_incomes)
        self.OnlyExpenses.clicked.connect(self.show_expenses)

        self.__update()

    def show_incomes(self):
        self.pie_chart.transaction_type = INCOME
        self.pie_chart.upd()

    def show_expenses(self):
        self.pie_chart.transaction_type = SPEND
        self.pie_chart.upd()

    def __update(self):
        self.pie_chart.upd()
        self._update_monthly()

    def _update_monthly(self):
        self.MonthlyIncomeMoney.setText(str(self.user.monthly_income) + ' ₽')
        self.MonthlyExpensesMoney.setText(str(self.user.monthly_spend) + ' ₽')

    def show_add_account_dialog(self):
        self.add_account_dialog = NewAccountDialog(self.user)
        self.add_account_dialog.exec()

    def show_accounts_filter_dialog(self):
        self.accounts_filter_dialog = AccountsFilterDialog(self.user)
        self.accounts_filter_dialog.exec()
        self.pie_chart.upd()

    def show_add_transaction_dialog(self):
        self.add_transaction_dialog = TransactionAddDialog(self.user)
        self.add_transaction_dialog.exec()
        self.pie_chart.upd()

    def show_transactions_history_dialog(self):
        self.transactions_history_dialog = TransactionsHistoryDialog(self.user)
        self.transactions_history_dialog.exec()
