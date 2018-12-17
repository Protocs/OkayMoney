import sys
import os.path


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
            return '...'
        return text[:max_length - 3] + '...'


INCOME = 'i'
SPEND = 's'

THEMES = {'standard': ['#EA005E', '#19b5fe', '#a0e300', '#ff5736', '#0078d7', '#f78fb3', '#db0dca',
                       '#f39c12', '#f9d9f4', '#00ffea'],
          'light': ['#f8007c', '#34edff', '#e1fb00', '#ff9767', '#00bff8', '#f9a0c4', '#f91cf5',
                    '#fdde26', '#fef9fe', '#00ffcf'],
          'hard': ['#b9003c', '#1078f8', '#68ad00', '#ff3823', '#004d9c', '#d95b77', '#a1088d',
                   '#cd650c', '#e09ed0', '#00ff3f']}


def mix_dicts(dicts):
    """Сливает словари из итератора в один и возвращает его."""
    big = next(dicts).copy()
    for d in dicts:
        big.update(d)
    return big


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


SPEND_ICONS = {
    "Одежда": "clothes",
    "Развлечения": "entertainment",
    "Еда": "food",
    "Дом": "house",
    "Транспорт": "transport",
    "Продукты": "foodstuff"
}
INCOME_ICONS = {"Денежный перевод": "card", "Заработная плата": "salary"}

for icons_dict in (SPEND_ICONS, INCOME_ICONS):
    for k, v in icons_dict.items():
        icons_dict[k] = find_data_file('ui/icons/' + v + '.png')
