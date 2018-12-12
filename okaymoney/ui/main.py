from ..util import INCOME, SPEND
from .messagebox import information
from .ui_window import UIWindow
from .widgets.pie_chart import PieChart
from .dialogs.new_account import NewAccountDialog
from .dialogs.accounts_filter import AccountsFilterDialog
from .dialogs.transaction_add import TransactionAddDialog
from .dialogs.transactions_history import TransactionsHistoryDialog
from .dialogs.settings import SettingsDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

class MainWindow(UIWindow):
    """Основное окно приложения.

    *Файл интерфейса:* ``ui/main.ui``
    """

    ui_path = 'ui/main.ui'

    def __init__(self, user, login_window):
        try:
            super().__init__()

            self.user = user
            self.login_window = login_window

            self.add_account_btn.clicked.connect(self.show_add_account_dialog)
            self.accounts_filter_btn.clicked.connect(self.show_accounts_filter_dialog)
            self.new_transaction_btn.clicked.connect(self.show_add_transaction_dialog)
            self.transactions_history_btn.clicked.connect(self.show_transactions_history_dialog)
            self.settings_btn.mousePressEvent = self.show_settings_dialog
            self.logout_btn.mousePressEvent = self.logout

            self.update_user()

            self.pie_chart = PieChart(self.pie_place, self.user)

            self.OnlyIncomes.clicked.connect(self.show_incomes)
            self.OnlyExpenses.clicked.connect(self.show_expenses)

            self.__update()
        except Exception as e:
            print(e)

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
        if not self.user.accounts:
            information("У вас еще нет ни одного счета.", self)
            return
        self.accounts_filter_dialog = AccountsFilterDialog(self.user)
        self.accounts_filter_dialog.exec()
        self.__update()

    def show_add_transaction_dialog(self):
        if not self.user.accounts:
            information("У вас еще нет ни одного счета, на который можно было бы "
                        "добавить транзакцию.", self)
            return
        self.add_transaction_dialog = TransactionAddDialog(self.user)
        self.add_transaction_dialog.exec()
        self.__update()

    def show_transactions_history_dialog(self):
        if not any([acc.transactions for acc in self.user.accounts]):
            information("У вас еще не совершено ни одной транзакции!", self)
            return
        self.transactions_history_dialog = TransactionsHistoryDialog(self.user)
        self.transactions_history_dialog.exec()
        self.__update()

    def show_settings_dialog(self, event):
        self.settings_dialog = SettingsDialog(self.user)
        self.settings_dialog.exec()
        self.update_user()

    def update_user(self):
        scene = QGraphicsScene()
        self.icon.setScene(scene)
        image = QImage()
        image.loadFromData(QByteArray(self.user.avatar))
        scene.addItem(QGraphicsPixmapItem(QPixmap().fromImage(image.scaled(48, 48))))
        self.username.setText(self.user.name)

    def logout(self, event):
        self.close()
        self.login_window.show()