import pickle
from .ui import messagebox


def save(acc):
    """Сохраняет ``acc`` в файл по пути :attribute:`~okaymoney.account.User.SAVE_PATH`.

    >>> from okaymoney.user import User
    >>> import os.path
    >>> acc = User('User')
    >>> save(acc)  # Сохранился по пути 'User.okm'
    >>> os.path.isfile('User.okm')
    True
    """
    try:
        with open(acc.SAVE_PATH, 'w') as f:
            pickle.dump(acc, f, pickle.HIGHEST_PROTOCOL)
    except OSError as e:
        messagebox.error(f'Невозможно создать файл для сохранения профиля: {acc.SAVE_PATH}\n({e})')


def load(path):
    """Загружает профиль из файла по пути ``path`` и возвращает его.

    >>> from okaymoney.user import User
    >>> acc = User('User')
    >>> save(acc)  # Сохранился по пути 'User.okm'
    >>> load('User.okm')  # Загружаем обратно
    <User object at ...>
    """
    try:
        with open(path) as f:
            return pickle.load(f)
    except OSError as e:
        messagebox.error(f'Невозможно открыть файл профиля: {path}\n({e})')
    except pickle.PickleError as e:
        messagebox.error(f'Ошибка загрузки профиля: {path}\n({e})')
