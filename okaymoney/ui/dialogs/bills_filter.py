from .ui_dialog import UIDialog
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox


class BillsFilterDialog(UIDialog):
    """Диалог окна, показывающего всех пользователей.

    *Файл интерфейса:* ``ui/dialogs/bills_filter_dialog.ui``
    """

    ui_path = 'ui/dialogs/bills_filter_dialog.ui'

    def __init__(self, user, checked_accounts):
        super().__init__()

        self.choose_bills_btn.clicked.connect(self.choose_bills)
        self.checkboxes = []
        self.checked_accounts = checked_accounts
        self.user = user

        for account in user.accounts:
            item = QListWidgetItem()
            self.bills_list.addItem(item)
            checkbox = QCheckBox(account.name, self)
            checkbox.setChecked(account in checked_accounts)
            self.checkboxes.append(checkbox)
            self.bills_list.setItemWidget(item, checkbox)

    def choose_bills(self):
        self.checked_accounts = [account for account in self.user.accounts if account.name in
                                 [checkbox.text() for checkbox in self.checkboxes if
                                  checkbox.isChecked()]]
        self.close()

    def get_checked_accounts(self):
        return self.checked_accounts
