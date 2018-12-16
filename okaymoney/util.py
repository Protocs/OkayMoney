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
THEMES = {'standard': ['#EA005E', '#3498db', '#8e44ad', '#f39c12', '#16a085', '#2ecc71', '#2c3e50',
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
