import calendar
from datetime import date, timedelta
from utils import find_date_at_weekday_before_date


class Stats(object):
    def __init__(self, date_to_timedelta_map, start_of_week=calendar.SUNDAY):
        self.date_to_timedelta_map = date_to_timedelta_map
        self.start_of_week = start_of_week

    @property
    def day(self):
        return self.date_to_timedelta_map.get(today(), timedelta(0))

    @property
    def week(self):
        start_of_week = find_date_at_weekday_before_date(
            self.start_of_week, today()
        )
        result = timedelta()
        for i in range(0, 6):
            date_ = start_of_week + timedelta(days=i)
            if date_ in self.date_to_timedelta_map:
                result += self.date_to_timedelta_map[date_]
        return result

    @property
    def month(self):
        t = today()
        d = t.replace(day=1)
        result = timedelta()
        while True:
            if d in self.date_to_timedelta_map:
                result += self.date_to_timedelta_map[d]
            d += timedelta(days=1)
            if d.month != t.month:
                break
        return result


def today():
    return date.today()
