from .ui_dialog import UIDialog
from .user_registration import add_avatar
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from ...user_save_load import remove, save
from ..messagebox import error
from ..widgets.pie_chart import SPEND_COLORS

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
        remove(self.user, self)
        self.close()
        self.main_window.close()
        self.login_window.show()
        self.login_window.fill_users()

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

    def add_category(self, categories, categories_list, del_button, fill_function):
        if categories_list:
            spend_item = categories.item(len(categories_list) - 1)
            if not spend_item.text():
                error("Нельзя добавлять пустые категории.", self)
                return
            if categories.isPersistentEditorOpen(spend_item):
                categories.closePersistentEditor(spend_item)
                categories_list[-1] = spend_item.text()
                fill_function()
        item = QListWidgetItem()
        if len(categories_list) <= len(SPEND_COLORS):
            categories.addItem(item)
            categories.openPersistentEditor(item)
            categories.setCurrentItem(item)
            categories_list.append("")
            del_button.setEnabled(True)
        else:
            error(f"Максимальное допустимое количество категорий - {len(SPEND_COLORS)}", self)

    def delete_category(self, categories_list, categories, fill_function):
        categories_list.pop(categories.currentRow())
        fill_function()

    def apply_changes(self):
        try:
            last_spend_item = self.spend_categories.item(len(self.spend_categories_list) - 1)
            last_income_item = self.income_categories.item(len(self.income_categories_list) - 1)
            if (last_spend_item and not last_spend_item.text()) \
                    or (last_income_item and not last_income_item.text()):
                error("Нельзя добавлять пустые категории!", self)
                return

            remove(self.user, self)

            self.user.name = self.user_name.text()
            self.user.SAVE_PATH = self.user.name + '.okm'
            self.user.avatar = self.avatar

            if self.spend_categories_list:
                self.spend_categories_list[-1] = last_spend_item.text()
            if self.income_categories_list:
                self.income_categories_list[-1] = last_income_item.text()
            self.user.income_categories = self.income_categories_list
            self.user.spend_categories = self.spend_categories_list

            save(self.user, self)

            self.close()
        except Exception as e:
            print(e)
