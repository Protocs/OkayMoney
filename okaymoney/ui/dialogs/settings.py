from .ui_dialog import UIDialog
from .user_registration import add_avatar
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from ...user_save_load import remove, save


class SettingsDialog(UIDialog):
    """Диалог регистрации нового пользователя.

    *Файл интерфейса:* ``ui/dialogs/settings.ui``
    """

    ui_path = 'ui/dialogs/settings.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.avatar = self.user.avatar
        self.spend_categories_list = self.user.spend_categories.copy()
        self.income_categories_list = self.user.income_categories.copy()

        self.tabWidget.currentChanged.connect(self.change_window_size)
        self.tabWidget.setCurrentIndex(0)

        self.user_name.setText(self.user.name)
        self.choose_avatar.clicked.connect(self.get_avatar_path)
        self.delete_user_btn.clicked.connect(self.delete_user)

        self.fill_income_categories()
        self.fill_spend_categories()
        self.spend_categories.itemClicked.connect(
            lambda x: self.delete_spend_category_btn.setEnabled(True))
        self.income_categories.itemClicked.connect(
            lambda x: self.delete_income_category_btn.setEnabled(True))
        self.spend_categories.currentTextChanged.connect(self.change_item)
        self.income_categories.currentTextChanged.connect(self.change_item)
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

    def get_avatar_path(self):
        filename = QFileDialog.getOpenFileName(self, 'Выбрать аватар')
        if filename[0]:
            add_avatar(self, filename[0], self.choose_avatar)

    def delete_user(self):
        remove(self.user)
        self.close()
        self.main_window.close()
        # Открытие окна логина не реализовано.

    def fill_spend_categories(self):
        self.spend_categories.clear()
        self.spend_categories.addItems(self.spend_categories_list)
        self.delete_spend_category_btn.setEnabled(False)

    def fill_income_categories(self):
        self.income_categories.clear()
        self.income_categories.addItems(self.income_categories_list)
        self.delete_income_category_btn.setEnabled(False)

    def get_categories(self):
        obj = self.sender().objectName()
        if obj == "add_spend_category_btn":
            self.add_category(self.spend_categories, self.spend_categories_list,
                              self.delete_spend_category_btn, self.fill_spend_categories)

        elif obj == "add_income_category_btn":
            self.add_category(self.income_categories, self.income_categories_list,
                              self.delete_income_category_btn, self.fill_income_categories)
        elif obj == "delete_spend_category_btn":
            self.delete_category(self.spend_categories_list, self.spend_categories,
                                 self.fill_spend_categories)
        elif obj == "delete_income_category_btn":
            self.delete_category(self.income_categories_list, self.income_categories,
                                 self.fill_income_categories)

    def change_item(self):
        pass

    def add_category(self, categories, categories_list, del_button, fill_function):
        spend_item = categories.item(len(categories_list) - 1)
        if categories.isPersistentEditorOpen(spend_item):
            categories.closePersistentEditor(spend_item)
            categories_list[-1] = spend_item.text()
            fill_function()
        item = QListWidgetItem()
        categories.addItem(item)
        categories.openPersistentEditor(item)
        categories.setCurrentItem(item)
        categories_list.append("")
        del_button.setEnabled(True)

    def delete_category(self, categories_list, categories, fill_function):
        categories_list.pop(categories.currentRow())
        fill_function()

    def apply_changes(self):
        self.user.name = self.user_name.text()
        self.user.avatar = self.avatar

        self.spend_categories_list[-1] = self.spend_categories.item(
            len(self.spend_categories_list) - 1).text()
        self.income_categories_list[-1] = self.income_categories.item(
            len(self.income_categories_list) - 1).text()
        self.user.income_categories = self.income_categories_list
        self.user.spend_categories = self.spend_categories_list
        save(self.user, self)
        self.close()
