from datetime import date, timedelta


class Stats(object):
    def __init__(self, hours_per_day, ):
        self.hours_per_day = hours_per_day

    @property
    def day(self):
        return self.hours_per_day[today()]

    @property
    def week(self):
        t = today()
        start_of_week = t - timedelta(days=t.weekday() + 1)
        result = timedelta()
        for i in range(0, 6):
            date_ = start_of_week + timedelta(days=i)
            if date_ in self.hours_per_day:
                result += self.hours_per_day[date_]
        return result

    @property
    def month(self):
        t = today()
        d = t.replace(day=1)
        result = timedelta()
        while True:
            if d in self.hours_per_day:
                result += self.hours_per_day[d]
            d += timedelta(days=1)
            if d.month != t.month:
                break
        return result


def today():
    return date.today()
