from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtCore import QByteArray, Qt

from requests import RequestException

from ...util import shorten
from ...user_save_load import load, save
from ..main import MainWindow
from .ui_widget import UIWidget
from ...util import get_user_from_server
from .. import messagebox


class UserLoginButton(UIWidget):
    """Кнопка пользователя, при нажатии которой происходит вход в систему.

    *Файл интерфейса:* ``ui/widgets/user_login_button.ui``
    """

    ui_path = "ui/widgets/user_login_button.ui"

    def __init__(self, login_window, path):
        super().__init__()

        self.user = load(path + ".okm", login_window)
        self.name.setText(shorten(self.user.name, 40))
        self.name.setToolTip(self.user.name)
        self.verticalLayout.setAlignment(Qt.AlignCenter)

        scene = QGraphicsScene()
        self.icon.setScene(scene)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(self.user.avatar))
        scene.addItem(QGraphicsPixmapItem(pixmap))

        self.login_window = login_window

        self.icon.mousePressEvent = self.name.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        if self.user.vk_id:
            try:
                from_server = get_user_from_server(self.user.vk_id)
            except RequestException:
                messagebox.error(
                    "Невозможно получить ваши данные с сервера. Проверьте подключение к сети."
                )
                return
            if from_server:
                save(from_server, self, synchronize=False)
                self.user = load(self.user.SAVE_PATH, self.login_window)
        self.main = MainWindow(self.user, self.login_window)
        self.main.show()
        self.login_window.close()
