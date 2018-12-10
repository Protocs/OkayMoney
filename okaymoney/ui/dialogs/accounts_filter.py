from .ui_dialog import UIDialog
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox
from ...user_save_load import save


class AccountsFilterDialog(UIDialog):
    """Диалог окна, показывающего всех пользователей.

    *Файл интерфейса:* ``ui/dialogs/accounts_filter_dialog.ui``
    """

    ui_path = 'ui/dialogs/accounts_filter_dialog.ui'

    def __init__(self, user):
        super().__init__()

        self.choose_accounts_btn.clicked.connect(self.choose_accounts)
        self.checkboxes = []
        self.user = user

        for account in user.accounts:
            item = QListWidgetItem()
            self.accounts_list.addItem(item)
            checkbox = QCheckBox(account.name + ' - ' + str(account.money) + ' ₽', self)
            checkbox.setChecked(account.checked)
            self.checkboxes.append(checkbox)
            self.accounts_list.setItemWidget(item, checkbox)

    def choose_accounts(self):
        for account in self.user.accounts:
            account.checked = account.name in [' - '.join(checkbox.text().split(' - ')[:-1])
                                               for checkbox in self.checkboxes if checkbox.isChecked()]
        save(self.user, self)
        self.close()
