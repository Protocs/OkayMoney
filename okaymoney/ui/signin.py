from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog


class SignInWindow(QDialog):
    ui_path = "ui/dialogs/sign_in.ui"

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.web_engine = QWebEngineView(self)
        self.web_engine.resize(self.width(), self.height())
        url = "https://oauth.vk.com/authorize?" \
              "client_id=6975005" \
              "&redirect_uri=http://okaymoney.pythonanywhere.com/vk" \
              "&response_type=code" \
              "&v=5.95"
        self.web_engine.setUrl(QUrl(url))
        self.web_engine.urlChanged.connect(self.check_url)
        self.exec()

    def check_url(self, url):
        if url.toString().startswith("http://okaymoney.pythonanywhere.com/vk"):
            self.close()
