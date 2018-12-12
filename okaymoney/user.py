import os
from datetime import datetime

from .util import INCOME, SPEND


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
        self.negative_balance_information = True

        # Категории доходов и расходов
        self.income_categories = ['Заработная плата', 'Денежный перевод']
        self.spend_categories = ['Продукты', 'Одежда', 'ЖКХ', 'Развлечения', 'Транспорт']

        self.SAVE_PATH = name + '.okm'

    def _monthly(self, tr_type):
        transactions = sum((a.transactions for a in self.accounts if a.checked), [])
        month_transactions = (t for t in transactions if t.date.month() == datetime.now().month)
        return abs(sum(m.delta for m in month_transactions if m.type == tr_type))

    @property
    def monthly_income(self):
        return self._monthly(INCOME)

    @property
    def monthly_spend(self):
        return self._monthly(SPEND)


def get_user_names_in_current_dir():
    """Возвращает имена всех созданных пользователей (те, что в текущей папке)."""
    return [file.split('.')[0] for file in os.listdir('.') if file.endswith('.okm')]
