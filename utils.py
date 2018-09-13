from datetime import timedelta
from functools import wraps


def find_date_at_weekday_before_date(weekday, before_date):
    while True:
        if before_date.weekday() == weekday:
            return before_date
        before_date -= timedelta(days=1)


def memoize(func):
    cache = {}

    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap
