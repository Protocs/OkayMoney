from ...user import User
from ..main import MainWindow
from .ui_widget import UIWidget


class UserLoginButton(UIWidget):
    """Кнопка пользователя, при нажатии которой происходит вход в систему.

    *Файл интерфейса:* ``ui/widgets/user_login_button.ui``
    """

    ui_path = 'ui/widgets/user_login_button.ui'

    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.icon.mousePressEvent = self.name.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        self.main = MainWindow(User('abc', 0))
        self.main.show()
        self.login_window.close()
