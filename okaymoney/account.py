class Account:
    """Отдельный счёт со своим балансом, к примеру, банковский счёт, счёт на карточке, наличные..."""

    def __init__(self, name, money):
        """
        :param name: имя баланса.
        :param money: начальный баланс.
        """
        self.name = name
        self.money = money
        self.transactions = []

    def add_transaction(self, tr):
        """Добавляет транзакцию в историю и изменяет баланс.

        >>> from okaymoney.transaction import Transaction
        >>> tr = Transaction('Покупки', -200)
        >>> acc = Account('Наличные', 300)
        >>> acc.add_transaction(tr)
        >>> acc.money
        100
        >>> acc.transactions
        {0: <Transaction object at ...>}
        """
        self.transactions.append(tr)
        self.money += tr.delta
