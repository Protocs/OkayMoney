from ...user import get_user_names_in_current_dir
from .ui_dialog import UIDialog


class MoreUsersDialog(UIDialog):
    """Диалог окна, показывающего всех пользователей.

    *Файл интерфейса:* ``ui/dialogs/more_users_dialog.ui``
    """

    ui_path = 'ui/dialogs/more_users_dialog.ui'

    def __init__(self):
        super().__init__()

        for user in get_user_names_in_current_dir():
            self.listWidget.addItem(user)

        self.choose_user_btn.clicked.connect(self.choose_user)
        self.listWidget.itemDoubleClicked.connect(self.choose_user)

    def choose_user(self):
        print(self.more_users_dialog.listWidget.currentItem())
        # TODO
