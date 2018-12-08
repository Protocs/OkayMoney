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


def mix_dicts(dicts):
    """Сливает словари из итератора в один и возвращает его."""
    big = next(dicts).copy()
    for d in dicts:
        big.update(d)
    return big
