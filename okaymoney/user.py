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

    def _monthly(self, tr_type, month, year):
        now = datetime.now()
        if month is None:
            month = now.month
        if year is None:
            year = now.year

        transactions = sum((a.transactions for a in self.accounts if a.checked), [])
        month_transactions = (t for t in transactions
                              if t.date.date().month() == month and t.date.date().year() == year)
        return abs(sum(m.delta for m in month_transactions if m.type == tr_type))

    def get_monthly_income(self, month=None, year=None):
        return self._monthly(INCOME, month, year)

    def get_monthly_spend(self, month=None, year=None):
        return self._monthly(SPEND, month, year)


def get_user_names_in_current_dir():
    """Возвращает имена всех созданных пользователей (те, что в текущей папке)."""
    return [file.split('.')[0] for file in os.listdir('.') if file.endswith('.okm')]
