import pickle

from . import messagebox


class Account:
    """Класс аккаунта, который содержит всю информацию о пользователе."""

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.SAVE_PATH = name + '.okm'

    def save(self, path):
        """Сохраняет себя в файл по пути ``f``."""
        try:
            with open(path, 'w') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        except OSError as e:
            messagebox.error(f'Невозможно создать файл для сохранения профиля: {path}\n({e})')

    @staticmethod
    def load(path):
        """Загружает профиль из файла по пути ``f`` и возвращает его."""
        try:
            with open(path) as f:
                return pickle.load(f)
        except OSError as e:
            messagebox.error(f'Невозможно открыть файл профиля: {path}\n({e})')
        except pickle.PickleError as e:
            messagebox.error(f'Ошибка загрузки профиля: {path}\n({e})')
