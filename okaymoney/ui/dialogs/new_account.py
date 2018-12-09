from .ui_dialog import UIDialog
from ..messagebox import error
from decimal import Decimal
from ...account import Account
from ...user_save_load import save


class NewAccountDialog(UIDialog):
    """Диалог добавления нового счета.

    *Файл интерфейса:* ``ui/dialogs/new_account.ui``
    """

    ui_path = 'ui/dialogs/new_account.ui'

    def __init__(self, user, checked_accounts):
        super().__init__()

        self.user = user
        self.checked_accounts = checked_accounts
        self.add_account_button.clicked.connect(self.add_account)

    def add_account(self):
        name = self.name_account.text()
        balance = self.start_balance.text()
        try:
            balance = Decimal(balance)
            if not name:
                raise Exception

            account = Account(name, balance)
            self.user.accounts.append(account)
            self.checked_accounts.append(account)
            save(self.user)

            self.close()

        except Exception:
            error('Ошибка, попробуйте еще раз.', self)
