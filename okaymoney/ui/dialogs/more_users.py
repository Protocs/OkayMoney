from ..main import MainWindow
from ...user import get_user_names_in_current_dir
from .ui_dialog import UIDialog
from ... import user_save_load


class MoreUsersDialog(UIDialog):
    """Диалог окна, показывающего всех пользователей.

    *Файл интерфейса:* ``ui/dialogs/more_users_dialog.ui``
    """

    ui_path = "ui/dialogs/more_users_dialog.ui"

    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        for user in get_user_names_in_current_dir():
            self.listWidget.addItem(user)

        self.choose_user_btn.clicked.connect(self.choose_user)
        self.listWidget.itemDoubleClicked.connect(self.choose_user)

    def choose_user(self):
        username = self.listWidget.currentItem().text()
        self.main = MainWindow(
            user_save_load.load(username + ".okm", self), self.login_window
        )
        self.main.show()
        self.close()
        self.login_window.close()
