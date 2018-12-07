from PIL import Image
from PyQt5.QtWidgets import QFileDialog

from ..messagebox import error
from .ui_dialog import UIDialog
from ...user import User, get_user_names_in_current_dir
from ...user_save_load import save


class UserRegistrationDialog(UIDialog):
    """Диалог регистрации нового пользователя.

    *Файл интерфейса:* ``ui/dialogs/user_registration.ui``
    """

    ui_path = 'ui/dialogs/user_registration.ui'

    def __init__(self):
        super().__init__()
        self.avatar = 'ui/default.png'

        self.ok_button.clicked.connect(self.create_user)
        self.cancel_button.clicked.connect(self.close)
        self.add_avatar_btn.clicked.connect(self.add_avatar)

    def create_user(self):
        name = self.name.text()
        if name:
            if name in get_user_names_in_current_dir():
                error('Пользователь с таким именем уже существует', self)
                return

            acc = User(name, self.avatar)
            save(acc)

            self.close()
        else:
            error('Введите имя пользователя', self)

    def add_avatar(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Выбрать аватар')
            image = Image.open(filename[0])
            if image.size[0] == 128 and image.size[1] == 128:
                self.avatar = filename[0]
                self.avatar_name.setText(filename[0].split('/')[-1])
            else:
                raise Exception
        except:
            error('Ошибка, попробуйте загрузить картинку снова.', self)
