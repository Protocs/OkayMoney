from decimal import Decimal


class User:
    """Класс пользователя, который содержит всю информацию о пользователе."""

    def __init__(self, name, balance):
        """
        :param name: имя пользователя.
        :param balance: начальный баланс.
        """
        self.name = name
        self.balance = Decimal(balance)
        self._accounts = []

        # Категории доходов и расходов
        self.income_categories = []
        self.spend_categories = []

        self.SAVE_PATH = name + '.okm'
