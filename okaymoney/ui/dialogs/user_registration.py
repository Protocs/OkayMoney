import requests
from PIL import Image
from PyQt5.QtWidgets import QFileDialog

from ...ui import messagebox
from .ui_dialog import UIDialog
from .signin import SignInDialog
from ...user import User, get_user_names_in_current_dir
from ...user_save_load import save
from ...util import (
    get_vk_user_info,
    get_avatar_from_url,
    save_app_token,
    get_user_from_server,
)


class UserRegistrationDialog(UIDialog):
    """Диалог регистрации нового пользователя.

    *Файл интерфейса:* ``ui/dialogs/user_registration.ui``
    """

    ui_path = "ui/dialogs/user_registration.ui"

    def __init__(self):
        super().__init__()
        with open("ui/default.png", "rb") as default:
            self.avatar = default.read()

        self.ok_button.clicked.connect(self.get_user_name)
        self.cancel_button.clicked.connect(self.close)
        self.add_avatar_btn.clicked.connect(self.get_avatar_path)
        self.login_vk.clicked.connect(self.login_with_vk)

    def get_user_name(self):
        name = self.name.text()
        create_user(self, name, self.avatar)

    def get_avatar_path(self):
        filename = QFileDialog.getOpenFileName(self, "Выбрать аватар")
        if filename[0]:
            add_avatar(self, filename[0], self.avatar_name)

    def login_with_vk(self):
        self.vw = SignInDialog()
        user_id, token, app_token = self.vw.exec()
        save_app_token(app_token, user_id)
        try:
            user_info = get_vk_user_info(user_id, token)
        except requests.RequestException:
            messagebox.error(
                "Не удалось получить ваши данные. Проверьте подключение к сети."
            )
            return
        avatar = get_avatar_from_url(user_info["photo_100"])
        name = " ".join([user_info["first_name"], user_info["last_name"]])
        create_user(self, name, avatar, user_id)


def create_user(obj, name, avatar, vk_id=None):
    """Создает пользователя name с аватаркой avatar в родительском виджете obj"""
    if name:
        if name in get_user_names_in_current_dir():
            messagebox.error("Пользователь с таким именем уже существует", obj)
            return
        if vk_id:
            acc = get_user_from_server(vk_id)
            if acc is None:
                acc = User(name, avatar, vk_id)
        else:
            acc = User(name, avatar, vk_id)
        save(acc, obj)

        obj.close()
    else:
        messagebox.error("Введите имя пользователя", obj)


def add_avatar(obj, avatar_path, avatar_name_widget):
    """
    Добавляет объекту obj атрибут avatar, содержащий аватарку в виде массива байтов
    и меняет текст виджета avatar_name_widget на имя аватарки.
    """
    try:
        image = Image.open(avatar_path)
        if image.size[0] == 128 and image.size[1] == 128:
            with open(avatar_path, "rb") as avatar:
                obj.avatar = avatar.read()
            avatar_name_widget.setText(avatar_path.split("/")[-1])
        else:
            raise Exception
    except Exception:
        messagebox.error("Ошибка, попробуйте загрузить картинку снова.", obj)
