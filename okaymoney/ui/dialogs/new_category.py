from .ui_dialog import UIDialog
from ..messagebox import error
from ...user_save_load import save


class NewCategoryDialog(UIDialog):
    """Диалог добавления новой категории.

    *Файл интерфейса:* ``ui/dialogs/new_category.ui``
    """

    ui_path = "ui/dialogs/new_category.ui"

    def __init__(self, categories_list, user):
        super().__init__()

        self.categories_list = categories_list
        self.user = user
        self.add_category_btn.clicked.connect(self.add_category)

    def add_category(self):
        name = self.category_name.text()
        try:
            if not name:
                error("Введите название категории", self)
                return
            if name in self.categories_list:
                error("Категория с таким названием уже существует", self)
                return
            if len(name) > 25:
                error("Длина названия категории не должна превышать 25 символов", self)
                return

            self.categories_list.append(name)
            save(self.user, self)

            self.close()

        except Exception:
            error("Ошибка, попробуйте еще раз.", self)
