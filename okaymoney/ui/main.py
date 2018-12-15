from datetime import datetime

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QListWidgetItem

from ..util import INCOME, SPEND
from .messagebox import information
from .ui_window import UIWindow
from .widgets.pie_chart import PieChart
from .dialogs.new_account import NewAccountDialog
from .dialogs.accounts_filter import AccountsFilterDialog
from .dialogs.transaction_add import TransactionAddDialog
from .dialogs.transactions_history import TransactionsHistoryDialog
from .dialogs.settings import SettingsDialog
from ..util import shorten


class MainWindow(UIWindow):
    """Основное окно приложения.

    *Файл интерфейса:* ``ui/main.ui``
    """

    ui_path = 'ui/main.ui'

    def __init__(self, user, login_window):
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

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.previousMonth.clicked.connect(self.show_prev_month)
        self.nextMonth.clicked.connect(self.show_next_month)
        self.toToday.clicked.connect(self.show_today)

        self.__update()

    @property
    def transactions(self):
        return any([acc.transactions for acc in self.user.accounts])

    def fill_accounts(self):
        self.accounts_list.clear()
        for acc in self.user.accounts:
            item = QListWidgetItem(
                "{}{}{} ₽".format(shorten(acc.name, 12), ' ' * (12 - len(acc.name)) + '\t',
                                  str(acc.money)))
            item.setToolTip(acc.name)
            self.accounts_list.addItem(item)

    def show_incomes(self):
        self.pie_chart.set_transaction_type(INCOME, self.month, self.year)

    def show_expenses(self):
        self.pie_chart.set_transaction_type(SPEND, self.month, self.year)

    def __update(self):
        self.pie_chart.upd(self.month, self.year)
        self._update_monthly()
        self.fill_accounts()
        self.dateLabel.setText(f'{str(self.month).zfill(2)}.{self.year}')

    def _update_monthly(self):
        self.MonthlyIncomeMoney.setText(str(self.user.get_monthly_income(self.month, self.year)) + ' ₽')
        self.MonthlyExpensesMoney.setText(str(self.user.get_monthly_spend(self.month, self.year)) + ' ₽')

    def show_add_account_dialog(self):
        self.add_account_dialog = NewAccountDialog(self.user)
        self.add_account_dialog.exec()
        self.fill_accounts()

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
        if not self.transactions:
            information("У вас еще не совершено ни одной транзакции!", self)
            return
        self.transactions_history_dialog = TransactionsHistoryDialog(self.user, self)
        self.transactions_history_dialog.exec()
        self.__update()

    def show_settings_dialog(self, event):
        self.settings_dialog = SettingsDialog(self.user, self.login_window, self)
        self.settings_dialog.exec()
        self.__update()
        self.update_user()

    def update_user(self):
        scene = QGraphicsScene()
        self.icon.setScene(scene)
        image = QImage()
        image.loadFromData(QByteArray(self.user.avatar))
        scene.addItem(QGraphicsPixmapItem(QPixmap().fromImage(image.scaled(48, 48))))
        self.username.setText(shorten(self.user.name, 20))
        self.username.setToolTip(self.user.name)

    def logout(self, event):
        self.close()
        self.login_window.show()
        self.login_window.fill_users()

    def show_prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.__update()

    def show_next_month(self):
        now = datetime.now()
        if (self.month, self.year) == (now.month, now.year):
            return

        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.__update()

    def show_today(self):
        now = datetime.now()
        self.month, self.year = now.month, now.year
        self.__update()
