from .ui_window import UIWindow
from .dialogs.user_registration import UserRegistrationDialog
from .dialogs.more_users import MoreUsersDialog
from ..user import get_user_names_in_current_dir
from .widgets.user_login_button import UserLoginButton


# noinspection PyAttributeOutsideInit
class LoginWindow(UIWindow):
    """Класс окна входа в приложение.

    *Файл интерфейса:* ``ui/login.ui``
    """

    ui_path = 'ui/login.ui'

    def __init__(self):
        super().__init__()

        self.add_account.clicked.connect(self.show_add_user_dialog)
        self.show_more_users_btn.clicked.connect(self.show_more_users_dialog)

        self.avatar = None

        self.fill_users()

    def clear_login_buttons_layout(self):
        """Убирает все кнопки пользователей."""
        for i in reversed(range(self.login_buttons_layout.count())):
            self.login_buttons_layout.itemAt(i).widget().deleteLater()

    def fill_users(self):
        """Перезаполняет окно кнопками пользователей."""
        self.clear_login_buttons_layout()

        users = get_user_names_in_current_dir()

        self.show_more_users_btn.setVisible(len(users) > 5)

        for user in users[:5]:
            button = UserLoginButton(self, user)
            button.name.setText(user)
            self.login_buttons_layout.addWidget(button)

    def show_add_user_dialog(self):
        self.add_user_dialog = UserRegistrationDialog()
        self.add_user_dialog.exec()
        self.fill_users()

    def show_more_users_dialog(self):
        self.more_users_dialog = MoreUsersDialog(self)
        self.more_users_dialog.exec()
