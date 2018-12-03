from .ui_window import UIWindow
from .dialogs.user_registration import UserRegistrationDialog
from okaymoney.user import User
from okaymoney.user_save_load import save
from .messagebox import error

class LoginWindow(UIWindow):
    """Класс окна входа в приложение.

    *Файл интерфейса:* ``ui/login.ui``
    """

    ui_path = 'ui/login.ui'

    def __init__(self):
        super().__init__()
        self.add_account.clicked.connect(self.show_add_user_dialog)


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
            acc = User(name, 0)
            save(acc)
            self.add_user_dialog.hide()
        else:
            error('Введите имя пользователя', self.add_user_dialog)

    def close_dialog(self):
        self.add_user_dialog.hide()


