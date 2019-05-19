from requests import RequestException

from okaymoney.ui import messagebox
from okaymoney.user_save_load import save, load
from okaymoney.util import get_user_from_server
from ..main import MainWindow
from ...user import get_user_names_in_current_dir
from .ui_dialog import UIDialog


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
        user = load(username + ".okm", self)
        if user.vk_id:
            try:
                from_server = get_user_from_server(user.vk_id)
            except RequestException:
                messagebox.error(
                    "Невозможно получить ваши данные с сервера. Проверьте подключение к сети.")
                return
            if from_server:
                save(from_server, self, synchronize=False)
                user = load(user.SAVE_PATH, self.login_window)
        self.main = MainWindow(user, self.login_window)
        self.main.show()
        self.close()
        self.login_window.close()
