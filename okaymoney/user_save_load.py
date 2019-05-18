import pickle
from .ui import messagebox
import os
import requests
import base64
from .util import get_app_token


def save(acc, obj):
    """Сохраняет ``acc`` в файл по пути :attribute:`~okaymoney.account.User.SAVE_PATH`.

    >>> from okaymoney.user import User
    >>> import os.path
    >>> acc = User('User')
    >>> save(acc)  # Сохранился по пути 'User.okm'
    >>> os.path.isfile('User.okm')
    True
    """
    try:
        with open(acc.SAVE_PATH, "wb") as f:
            pickle.dump(acc, f, pickle.HIGHEST_PROTOCOL)
    except OSError as e:
        messagebox.error(
            f"Невозможно создать файл для сохранения профиля: {acc.SAVE_PATH}\n({e})",
            obj,
        )
    if acc.vk_id:
        account_pickle = pickle.dumps(acc, pickle.HIGHEST_PROTOCOL)
        account_base64 = base64.b64encode(account_pickle)
        app_token = get_app_token(acc.vk_id)
        try:
            requests.post(
                "http://okaymoney.pythonanywhere.com/user/"
                + str(acc.vk_id)
                + f"?token={app_token}",
                account_base64,
            )
        except requests.RequestException:
            messagebox.warning(
                "Не удалось синхронизировать ваш аккаунт с сервером. "
                "Проверьте подключение к сети."
            )


def load(path, obj):
    """Загружает профиль из файла по пути ``path`` и возвращает его.

    >>> from okaymoney.user import User
    >>> acc = User('User')
    >>> save(acc)  # Сохранился по пути 'User.okm'
    >>> load('User.okm')  # Загружаем обратно
    <User object at ...>
    """
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except OSError as e:
        messagebox.error(f"Невозможно открыть файл профиля: {path}\n({e})", obj)
    except pickle.PickleError as e:
        messagebox.error(f"Ошибка загрузки профиля: {path}\n({e})", obj)


def remove(acc, obj):
    """Удаляет файл пользователя acc"""
    if acc.vk_id:
        app_token = get_app_token(acc.vk_id)
        try:
            requests.delete(
                "http://okaymoney.pythonanywhere.com/user/"
                + str(acc.vk_id)
                + f"?token={app_token}"
            )
        except requests.RequestException:
            messagebox.warning(
                "Не удалось удалить ваш аккаунт с сервера. "
                "Чтобы удалить аккаунт с сервера, проверьте подключение к сети, "
                "затем снова войдите в аккаунт через ВК и повторите удаление."
            )
    try:
        os.remove(acc.SAVE_PATH)
    except Exception as e:
        messagebox.error(
            f"Невозможно удалить файл по пути: {acc.SAVE_PATH}\n({e})", obj
        )
