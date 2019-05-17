import os
from datetime import datetime

from .util import INCOME, SPEND


class User:
    """Класс пользователя, который содержит всю информацию о пользователе."""

    def __init__(self, name, avatar, vk_id):
        """
        :param name: имя пользователя.
        :param avatar: аватарка в виде массива байтов.
        :param vk_id: ID пользователя в ВКонтакте.
        """
        self.name = name
        self.accounts = []
        self.avatar = avatar
        self.vk_id = vk_id
        self.negative_balance_information = True
        self.theme = "standard"

        # Категории доходов и расходов
        self.income_categories = ["Заработная плата", "Денежный перевод"]
        self.spend_categories = [
            "Продукты",
            "Одежда",
            "Дом",
            "Развлечения",
            "Транспорт",
            "Еда",
        ]

        self.SAVE_PATH = name + ".okm"

    def _monthly(self, tr_type, month, year):
        now = datetime.now()
        if month is None:
            month = now.month
        if year is None:
            year = now.year

        transactions = sum((a.transactions for a in self.accounts if a.checked), [])
        month_transactions = (
            t
            for t in transactions
            if t.date.date().month() == month and t.date.date().year() == year
        )
        return abs(sum(m.delta for m in month_transactions if m.type == tr_type))

    def get_monthly_income(self, month=None, year=None):
        return self._monthly(INCOME, month, year)

    def get_monthly_spend(self, month=None, year=None):
        return self._monthly(SPEND, month, year)


def get_user_names_in_current_dir():
    """Возвращает имена всех созданных пользователей (те, что в текущей папке)."""
    return list(
        sorted(
            (file.split(".")[0] for file in os.listdir(".") if file.endswith(".okm")),
            key=lambda f: os.stat(f + ".okm").st_mtime,
            reverse=True,
        )
    )
