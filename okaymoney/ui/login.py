from .ui_window import UIWindow
from .dialogs.user_registration import UserRegistrationDialog
from .dialogs.more_users import MoreUsersDialog
from okaymoney.user import User
from okaymoney.user_save_load import save, load
from .messagebox import error
from .widgets.user_login_button import UserLoginButton
import os


class LoginWindow(UIWindow):
    """Класс окна входа в приложение.

    *Файл интерфейса:* ``ui/login.ui``
    """

    ui_path = 'ui/login.ui'

    def __init__(self):
        super().__init__()
        self.add_account.clicked.connect(self.show_add_user_dialog)
        self.show_more_users_btn.clicked.connect(self.show_more_users_dialog)
        self.users = [file[:file.find('.okm')] for file in os.listdir() if '.okm' in file]
        if len(self.users) <= 5:
            self.show_more_users_btn.hide()
        if len(self.users) > 0:
            for user in self.users[:5]:
                self.show_user(user)

    def show_add_user_dialog(self):
        self.add_user_dialog = UserRegistrationDialog()
        self.add_user_dialog.ok_button.clicked.connect(self.add_user)
        self.add_user_dialog.cancel_button.clicked.connect(self.close_dialog)
        self.add_user_dialog.exec()

    def show_more_users_dialog(self):
        self.more_users_dialog = MoreUsersDialog()
        for user in self.users:
            self.more_users_dialog.listWidget.addItem(user)
        self.more_users_dialog.choose_user_btn.clicked.connect(self.choose_user)
        self.more_users_dialog.listWidget.itemDoubleClicked.connect(self.choose_user)
        self.more_users_dialog.exec()

    def choose_user(self):
        selected = self.more_users_dialog.listWidget.currentItem()

    def add_user(self):
        name = self.add_user_dialog.name.text()
        if name:
            if name in self.users:
                error('Пользователь с таким именем уже существует', self.add_user_dialog)
                return
            acc = User(name, 0)
            save(acc)
            self.add_user_dialog.hide()
            self.users.append(name)
            if len(self.users) >= 6:
                self.show_more_users_btn.show()
            else:
                self.show_user(name)

        else:
            error('Введите имя пользователя', self.add_user_dialog)

    def close_dialog(self):
        self.add_user_dialog.hide()

    def show_user(self, user):
        button = UserLoginButton(self)
        button.name.setText(user)
        button.name.setToolTip(user)
        self.login_buttons_layout.addWidget(button)
