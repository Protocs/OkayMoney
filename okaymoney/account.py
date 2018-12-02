import pickle

from . import messagebox


class Account:
    """Класс аккаунта, который содержит всю информацию о пользователе."""

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.SAVE_PATH = name + '.okm'

    def add_transaction(self, tr):
        """Добавляет транзакцию в историю и изменяет баланс."""
        self._transactions.append(tr)
        self.money += tr.delta
