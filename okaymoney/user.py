import os


class User:
    """Класс пользователя, который содержит всю информацию о пользователе."""

    def __init__(self, name, avatar_path):
        """
        :param name: имя пользователя.
        :param avatar_path: путь до аватарки.
        """
        self.name = name
        self.accounts = []
        self.avatar_path = avatar_path

        # Категории доходов и расходов
        self.income_categories = []
        self.spend_categories = []

        self.SAVE_PATH = name + '.okm'


def get_user_names_in_current_dir():
    """Возвращает имена всех созданных пользователей (те, что в текущей папке)."""
    return [file.split('.')[0] for file in os.listdir('.') if file.endswith('.okm')]
