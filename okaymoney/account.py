from .transaction_list import TransactionList


class Account:
    """Отдельный счёт со своим балансом, к примеру, банковский счёт, счёт на карточке, наличные..."""

    def __init__(self, name, money):
        """
        :param name: имя баланса.
        :param money: начальный баланс.
        """
        self.name = name
        self.money = money
        self._transactions = TransactionList()

    def add_transaction(self, tr):
        """Добавляет транзакцию в историю и изменяет баланс."""
        self._transactions.append(tr)
        self.money += tr.delta
