from .ui_window import UIWindow


class LoginWindow(UIWindow):
    """Класс окна входа в приложение.

    *Файл интерфейса:* ``ui/login.ui``
    """

    ui_path = 'ui/login.ui'

    def __init__(self):
        super().__init__()
        ...
