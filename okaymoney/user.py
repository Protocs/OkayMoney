import os


class User:
    """Класс пользователя, который содержит всю информацию о пользователе."""

    def __init__(self, name, avatar):
        """
        :param name: имя пользователя.
        :param avatar: аватарка в виде массива байтов.
        """
        self.name = name
        self.accounts = []
        self.avatar = avatar

        # Категории доходов и расходов
        self.income_categories = ['Заработная плата', 'Денежный перевод']
        self.spend_categories = ['Продукты', 'Одежда', 'ЖКХ', 'Развлечения', 'Транспорт']

        self.SAVE_PATH = name + '.okm'


def get_user_names_in_current_dir():
    """Возвращает имена всех созданных пользователей (те, что в текущей папке)."""
    return [file.split('.')[0] for file in os.listdir('.') if file.endswith('.okm')]
