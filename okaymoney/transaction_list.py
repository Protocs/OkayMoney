class TransactionList(dict):
    """Список транзакций, где каждая из них имеет свой id.

    Имеет вид словаря, где ключи - id, а значения - транзакции.
    """

    def __init__(self):
        super().__init__()

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
