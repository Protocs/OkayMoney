class TransactionList(dict):
    """Список транзакций, где каждая из них имеет свой id.

    Имеет вид словаря, где ключи - id, а значения - транзакции.
    """

    def __init__(self, d=None):
        super().__init__(d if d is not None else {})

        # id последней транзакции
        self.last_id = -1

    def _next_id(self):
        """Возвращает id для следующей транзакции."""
        self.last_id += 1
        return self.last_id

    def append(self, tr):
        """
        >>> from okaymoney.transaction import Transaction
        >>> tr_list = TransactionList()
        >>> trans = Transaction('Покупки', -200)
        >>> tr_list.append(trans)
        >>> tr_list
        {0: <Transaction object at ...>}
        """
        new_id = self._next_id()
        self[new_id] = tr

    def merge(self):
        """
        Объединяет транзакции одинаковых категорий в большие, по одной на категорию.
        Используется в :class:`~okaymoney.widgets.PieChart`.

        :return: транзакции в формате для :class:`~okaymoney.widgets.PieChart`.
        """
        categories = {t.category for t in self}
        big_transactions = []

        for c in categories:
            transactions_of_category = (t for t in self if t.category == c)
            deltas = (t.delta for t in transactions_of_category)
            big_transactions.append((c, sum(deltas)))

        return big_transactions

    def filter(self, income_or_spend=None, *, categories=None):
        """Возвращает отфильтрованный :class:`TransactionList`."""
        def income_or_spend_key(t):
            if income_or_spend is None:
                return True
            return t.type == income_or_spend

        def category_key(t):
            if categories is None:
                return True
            return t.category in categories

        return TransactionList({k: v for (k, v) in self.values() if income_or_spend_key(v) and category_key(v)})
