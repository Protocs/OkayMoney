from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

from ...user_save_load import load
from ..main import MainWindow
from .ui_widget import UIWidget


class UserLoginButton(UIWidget):
    """Кнопка пользователя, при нажатии которой происходит вход в систему.

    *Файл интерфейса:* ``ui/widgets/user_login_button.ui``
    """

    ui_path = 'ui/widgets/user_login_button.ui'

    def __init__(self, login_window, path):
        super().__init__()

        self.user = load(path + '.okm')
        self.name.setText(self.user.name)

        scene = QGraphicsScene()
        self.icon.setScene(scene)
        pix_item = QGraphicsPixmapItem(QPixmap(self.user.avatar_path))
        scene.addItem(pix_item)

        self.login_window = login_window

        self.icon.mousePressEvent = self.name.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        self.main = MainWindow(self.user)
        self.main.show()
        self.login_window.close()
