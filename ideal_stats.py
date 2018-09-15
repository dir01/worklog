from datetime import timedelta, date

from utils import find_date_at_weekday_before_date


class IdealStats(object):
    def __init__(self, hours_per_day, work_weekdays, holidays=None):
        self.hours_per_day = hours_per_day
        self.work_weekdays = work_weekdays
        self.holidays = holidays or {}

    @property
    def day(self):
        return timedelta(hours=self.hours_per_day)

    @property
    def week(self):
        dt = find_date_at_weekday_before_date(
            weekday=self.work_weekdays[0],
            before_date=today()
        )
        return self.get_timedelta_for_workdays_since_date(dt)

    @property
    def month(self):
        dt = today().replace(day=1)
        return self.get_timedelta_for_workdays_since_date(dt)

    def get_timedelta_for_workdays_since_date(self, dt):
        delta = timedelta()
        while dt <= today():
            if dt in self.holidays:
                delta += self.holidays[dt]
            elif dt.weekday() in self.work_weekdays:
                delta += self.day
            dt += timedelta(days=1)
        return delta


def today():
    return date.today()
