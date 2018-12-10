from .util import INCOME, SPEND


class Transaction:
    """Доход или расход."""

    def __init__(self, category, delta, date, note):
        """
        :param category: категория транзакции.
        :param delta: изменение баланса. Положительное число - доход, отрицательное - расход.
        """
        if not delta:
            raise ValueError('бесполезная транзакция: дельта == 0')

        self.category = category
        self.delta = delta
        self.date = date
        self.note = note

    @property
    def type(self):
        """Тип транзакции: доход или расход."""
        return INCOME if self.delta > 0 else SPEND

    def to_pie_data(self):
        """
        Переводит транзакцию в формат ``(категория, abs(дельта))``
        для использования в :class:`~okaymoney.widgets.PieChart`.
        """
        return self.category, abs(self.delta)

    def __add__(self, other):
        """Сливает транзакции в одну."""
        if self.category != other.category:
            raise ValueError('невозможно слить транзакции разных категорий')

        return Transaction(self.category, self.delta + other.delta, None, None)
