from datetime import timedelta, date


class IdealStats(object):
    def __init__(self, hours_per_day, work_weekdays):
        self.hours_per_day = hours_per_day
        self.work_weekdays = work_weekdays

    @property
    def day(self):
        return timedelta(hours=self.hours_per_day)

    @property
    def week(self):
        dt = self._find_date_at_weekday_before_date(
            weekday=self.work_weekdays[0],
            before_date=today()
        )
        delta = timedelta()
        while dt <= today():
            if dt.weekday() in self.work_weekdays:
                delta += self.day
            dt += timedelta(days=1)
        return delta

    @property
    def month(self):
        dt = today().replace(day=1)
        delta = timedelta()
        while dt <= today():
            if dt.weekday() in self.work_weekdays:
                delta += self.day
            dt += timedelta(days=1)
        return delta

    def _find_date_at_weekday_before_date(self, weekday, before_date):
        while True:
            if before_date.weekday() == weekday:
                return before_date
            before_date -= timedelta(days=1)


def today():
    return date.today()
