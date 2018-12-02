class Transaction:
    """Доход или расход."""

    def __init__(self, category, delta, date, note):
        """
        :param category: категория транзакции.
        :param delta: изменение баланса. Положительное число - доход, отрицательное - расход.
        """
        self.category = category
        self.delta = delta
        self.date = date
        self.note = note
