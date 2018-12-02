class Transaction:
    """Доход или расход."""

    def __init__(self, category, delta):
        """
        :param category: категория транзакции.
        :param delta: изменение баланса. Положительное число - доход, отрицательное - расход.
        """
        self.category = category
        self.delta = delta
