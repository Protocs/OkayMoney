import base64
import json
import pickle

import requests


def shorten(text, max_length):
    """Сокращает текст таким образом, чтобы его длина не превышала ``max_length``.

    >>> shorten('1234', 5)
    '1234'
    >>> shorten('123456789', 5)
    '12...'
    """
    if len(text) <= max_length:
        return text
    else:
        if max_length < 3:
            return "..."
        return text[: max_length - 3] + "..."


INCOME = "i"
SPEND = "s"

THEMES = {
    "standard": [
        "#EA005E",
        "#19b5fe",
        "#a0e300",
        "#ff5736",
        "#0078d7",
        "#f78fb3",
        "#db0dca",
        "#f39c12",
        "#f9d9f4",
        "#00ffea",
    ],
    "light": [
        "#f8007c",
        "#34edff",
        "#e1fb00",
        "#ff9767",
        "#00bff8",
        "#f9a0c4",
        "#f91cf5",
        "#fdde26",
        "#fef9fe",
        "#00ffcf",
    ],
    "hard": [
        "#b9003c",
        "#1078f8",
        "#68ad00",
        "#ff3823",
        "#004d9c",
        "#d95b77",
        "#a1088d",
        "#cd650c",
        "#e09ed0",
        "#00ff3f",
    ],
}

SPEND_ICONS = {
    "Одежда": "ui/icons/clothes.png",
    "Развлечения": "ui/icons/entertainment.png",
    "Еда": "ui/icons/food.png",
    "Дом": "ui/icons/house.png",
    "Транспорт": "ui/icons/transport.png",
    "Продукты": "ui/icons/foodstuff.png",
}
INCOME_ICONS = {
    "Денежный перевод": "ui/icons/card.png",
    "Заработная плата": "ui/icons/salary.png",
}
OTHER_ICON = "ui/icons/other.png"

MONTHS = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]


def mix_dicts(dicts):
    """Сливает словари из итератора в один и возвращает его."""
    big = next(dicts).copy()
    for d in dicts:
        big.update(d)
    return big


def get_vk_user_info(user_id, token):
    request_uri = f"https://api.vk.com/method/users.get"
    response = requests.get(
        request_uri,
        params={
            "access_token": token,
            "v": "5.95",
            "fields": "first_name," "last_name,photo_100",
            "user_ids": str(user_id),
        },
    )
    json_format = json.loads(response.content)["response"][0]
    return json_format


def get_avatar_from_url(url):
    response = requests.get(url)
    return response.content


def save_app_token(token, user_id):
    with open("users.json", "w+", encoding="utf-8") as f:
        if f.read():
            json_data = json.load(f)
            json_data.update({user_id: token})
        else:
            json_data = {user_id: token}
        json.dump(json_data, f)


def get_app_token(user_id):
    with open("users.json", encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data.get(str(user_id))


def get_user_from_server(vk_id):
    request = requests.get(
        "http://okaymoney.pythonanywhere.com/user/"
        + str(vk_id)
        + f"?token={get_app_token(vk_id)}"
    )
    if request.content:
        acc_pickle = base64.b64decode(request.content)
        acc = pickle.loads(acc_pickle)
        return acc
