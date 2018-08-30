class Formatter(object):
    def __init__(self, stats, ideal):
        self.stats = stats
        self.ideal = ideal

    @property
    def day(self):
        return self._format('day')

    @property
    def week(self):
        return self._format('week')

    @property
    def month(self):
        return self._format('month')

    def _format(self, attr):
        passed = getattr(self.stats, attr)
        ideal = getattr(self.ideal, attr)

        def f(td):
            total_minutes = td.total_seconds() / 60
            hours = int(total_minutes / 60)
            minutes = int(total_minutes - (hours * 60))
            return '%.2d:%.2d' % (hours, minutes)

        return '{} of {}'.format(f(passed), f(ideal))
