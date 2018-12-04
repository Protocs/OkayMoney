from .ui_window import UIWindow
from .dialogs.user_registration import UserRegistrationDialog
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
        self.users = []
        self.show_users()

    def show_add_user_dialog(self):
        self.add_user_dialog = UserRegistrationDialog()
        self.add_user_dialog.checkBox.stateChanged.connect(self.change_state)
        self.add_user_dialog.password.setEnabled(False)
        self.add_user_dialog.repeat_password.setEnabled(False)
        self.add_user_dialog.ok_button.clicked.connect(self.add_user)
        self.add_user_dialog.cancel_button.clicked.connect(self.close_dialog)
        self.add_user_dialog.exec_()

    def change_state(self):
        checked = self.sender().isChecked()
        self.add_user_dialog.password.setEnabled(checked)
        self.add_user_dialog.repeat_password.setEnabled(checked)

    def add_user(self):
        name = self.add_user_dialog.name.text()
        if self.add_user_dialog.checkBox.isChecked():
            password = self.add_user_dialog.password.text()
            repeated_password = self.add_user_dialog.repeat_password.text()
            # Создание аккаунта с паролем не реализовано.
        if name:
            if name in [user for user in self.users]:
                error('Пользователь с таким именем уже существует', self.add_user_dialog)
                return
            acc = User(name, 0)
            save(acc)
            self.add_user_dialog.hide()
            self.show_users()
        else:
            error('Введите имя пользователя', self.add_user_dialog)

    def close_dialog(self):
        self.add_user_dialog.hide()

    def show_users(self):
        for file in os.listdir():
            if '.okm' in file:
                user = load(file)
                print(self.users, user.name)
                if user.name not in self.users:
                    button = UserLoginButton()
                    button.name.setText(user.name)
                    self.login_buttons_layout.addWidget(button)
                    self.users.append(user.name)
