from .ui.dialogs.confirm import ConfirmActionDialog
from .util import SPEND


class Account:
    """Отдельный счёт со своим балансом, к примеру, банковский счёт, счёт на карточке, наличные..."""

    def __init__(self, name, money):
        """
        :param name: имя баланса.
        :param money: начальный баланс.
        """
        self.name = name
        self.money = money
        self.checked = True
        self.transactions = []

    def add_transaction(self, tr, negative_balance_information):
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
        if self.money + tr.delta < 0 and negative_balance_information and tr.type == SPEND:
            msg = "После совершения этой операции баланс на счете станет отрицательным" \
                if self.money >= 0 else "Баланс вашего счета отрицательный"
            confirm_dialog = ConfirmActionDialog(msg)
            if not confirm_dialog.exec():
                return False
        self.transactions.append(tr)
        self.money += tr.delta
        self.transactions.sort(key=lambda e: e.date, reverse=True)
        return True

    def remove_transaction(self, tr, negative_balance_information):
        if tr not in self.transactions:
            raise ValueError('Транзакции не существует')
        if self.money - tr.delta < 0 and negative_balance_information and tr.type == SPEND:
            msg = "После удаления этой транзакции баланс на счете станет отрицательным" \
                if self.money >= 0 else "Баланс вашего счета отрицательный"
            confirm_dialog = ConfirmActionDialog(msg)
            if not confirm_dialog.exec():
                return False
        self.transactions.remove(tr)
        self.money -= tr.delta
        self.transactions.sort(key=lambda e: e.date, reverse=True)
        return True
