from .ui_window import UIWindow
from .widgets.pie_chart import PieChart
from .dialogs.new_bill import NewBillDialog
from .dialogs.bills_filter import BillsFilterDialog


class MainWindow(UIWindow):
    """Основное окно приложения.

    *Файл интерфейса:* ``ui/main.ui``
    """

    ui_path = 'ui/main.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.checked_accounts = []

        self.AddBill.clicked.connect(self.show_add_bill_dialog)
        self.AllBills.clicked.connect(self.show_bills_filter_dialog)

        PieChart(self.pie_place, self.checked_accounts)

    def show_add_bill_dialog(self):
        self.add_bill_dialog = NewBillDialog(self.user)
        self.add_bill_dialog.exec()

    def show_bills_filter_dialog(self):
        self.bills_filter_dialog = BillsFilterDialog(self.user, self.checked_accounts)
        self.bills_filter_dialog.exec()
        self.checked_accounts = self.bills_filter_dialog.get_checked_accounts()
