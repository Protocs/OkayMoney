from .ui_dialog import UIDialog
from .user_registration import add_avatar
from PyQt5.QtWidgets import QFileDialog
from ...user_save_load import remove, save
from ..messagebox import error
from .confirm import ConfirmActionDialog
from .new_category import NewCategoryDialog

class SettingsDialog(UIDialog):
    """Диалог настроек.

    *Файл интерфейса:* ``ui/dialogs/settings.ui``
    """

    ui_path = 'ui/dialogs/settings.ui'

    def __init__(self, user, login_window, main_window):
        super().__init__()

        self.user = user
        self.login_window = login_window
        self.main_window = main_window
        self.avatar = self.user.avatar

        self.tabWidget.currentChanged.connect(self.change_window_size)
        self.tabWidget.setCurrentIndex(0)

        self.user_name.setText(self.user.name)
        self.choose_avatar.clicked.connect(self.get_avatar_path)
        self.negative_balance_information.setChecked(self.user.negative_balance_information)
        self.negative_balance_information.stateChanged.connect(self.change_state)
        self.delete_user_btn.clicked.connect(self.delete_user)

        self.fill_income_categories()
        self.fill_spend_categories()
        self.spend_categories.currentItemChanged.connect(
            lambda x: self.delete_spend_category_btn.setEnabled(True))
        self.income_categories.currentItemChanged.connect(
            lambda x: self.delete_income_category_btn.setEnabled(True))
        self.delete_spend_category_btn.clicked.connect(self.get_categories)
        self.delete_income_category_btn.clicked.connect(self.get_categories)
        self.add_spend_category_btn.clicked.connect(self.get_categories)
        self.add_income_category_btn.clicked.connect(self.get_categories)

        self.ok_btn.clicked.connect(self.apply_changes)
        self.cancel_btn.clicked.connect(self.close)

    def change_window_size(self):
        if self.tabWidget.currentIndex() == 1:
            self.setMinimumSize(600, 350)
            self.resize(600, 350)
        else:
            self.setMinimumSize(420, 280)
            self.resize(420, 280)

    def change_state(self):
        self.user.negative_balance_information = self.negative_balance_information.isChecked()

    def get_avatar_path(self):
        filename = QFileDialog.getOpenFileName(self, 'Выбрать аватар')
        if filename[0]:
            add_avatar(self, filename[0], self.choose_avatar)

    def delete_user(self):
        self.confirm_dialog = ConfirmActionDialog(
            f'Вы действительно хотите удалить аккаунт пользователя '
            f'"{self.user.name}"?\nВсе данные будут стерты без возможности восстановления!')
        if self.confirm_dialog.exec():
            remove(self.user, self)
            self.close()
            self.main_window.close()
            self.login_window.show()
            self.login_window.fill_users()

    def fill_spend_categories(self):
        self.spend_categories.clear()
        self.spend_categories.addItems(self.user.spend_categories)
        self.delete_spend_category_btn.setEnabled(False)

    def fill_income_categories(self):
        self.income_categories.clear()
        self.income_categories.addItems(self.user.income_categories)
        self.delete_income_category_btn.setEnabled(False)

    def get_categories(self):
        obj = self.sender().objectName()
        if obj == "add_spend_category_btn":
            self.add_category(self.user.spend_categories, self.fill_spend_categories)
        elif obj == "add_income_category_btn":
            self.add_category(self.user.income_categories, self.fill_income_categories)
        elif obj == "delete_spend_category_btn":
            self.delete_category(self.user.spend_categories, self.spend_categories,
                                 self.fill_spend_categories)
        elif obj == "delete_income_category_btn":
            self.delete_category(self.user.income_categories, self.income_categories,
                                 self.fill_income_categories)

    def add_category(self, categories_list, fill_function):
        if len(categories_list) < 10:
            self.new_category_dialog = NewCategoryDialog(categories_list, self.user)
            self.new_category_dialog.exec()
            fill_function()
        else:
            error("Максимальное допустимое количество категорий - 10", self)

    def delete_category(self, categories_list, categories, fill_function):
        categories_list.pop(categories.currentRow())
        fill_function()

    def apply_changes(self):
        remove(self.user, self)

        self.user.name = self.user_name.text()
        self.user.SAVE_PATH = self.user.name + '.okm'
        self.user.avatar = self.avatar

        save(self.user, self)

        self.close()
