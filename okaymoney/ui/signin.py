import json

from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog


class SignInWindow(QDialog):
    ui_path = "ui/dialogs/sign_in.ui"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход через VK")
        self.setWindowIcon(QIcon("ui/vk_icon.png"))

        self.user_id = None
        self.access_token = None
        self.app_token = None

        self.setFixedSize(800, 600)
        self.web_engine = QWebEngineView(self)
        self.web_engine.resize(self.width(), self.height())
        url = (
            "https://oauth.vk.com/authorize?"
            "client_id=6975005"
            "&redirect_uri=http://okaymoney.pythonanywhere.com/vk"
            "&response_type=code"
            "&v=5.95"
            "&revoke=1"
        )
        self.web_engine.setUrl(QUrl(url))
        self.web_engine.loadFinished.connect(self.check_user_id)

    def check_user_id(self):
        if (
            self.web_engine.url()
            .toString()
            .startswith("http://okaymoney.pythonanywhere.com/vk")
        ):
            self.web_engine.page().toPlainText(self.get_plain_text)

    def get_plain_text(self, text):
        response = json.loads(text)
        self.user_id = response.get("user_id")
        self.access_token = response.get("access_token")
        self.app_token = response.get("app_token")
        self.close()

    def exec(self):
        super().exec()
        return self.user_id, self.access_token, self.app_token
