from calendar import SUNDAY, MONDAY, TUESDAY, WEDNESDAY

"""
Just for reference

    August 2018
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
"""
from datetime import date, timedelta
from unittest.mock import patch

from ideal_stats import IdealStats

stats = IdealStats(hours_per_day=9, work_weekdays=[SUNDAY, MONDAY, TUESDAY, WEDNESDAY])



class TestIdealStats(object):
    def test_day(self):
        assert stats.day == timedelta(hours=9)

    def test_week_at_sunday(self):
        with self.patch_today(12):
            assert stats.week == timedelta(hours=9)

    def test_week_at_wednsday(self):
        with self.patch_today(14):
            assert stats.week == timedelta(hours=3 * 9)

    def test_week_at_friday(self):
        with self.patch_today(17):
            assert stats.week == timedelta(hours=4 * 9)

    def test_month_at_first_week(self):
        with self.patch_today(4):
            assert stats.month == timedelta(hours=1 * 9)

    def test_month_at_the_middle(self):
        with self.patch_today(15):
            assert stats.month == timedelta(hours=9 * 9)

    def test_month_at_the_end(self):
        with self.patch_today(31):
            assert stats.month == timedelta(hours=17 * 9)

    def patch_today(self, day_of_month):
        return patch('ideal_stats.today', return_value=date(2018, 8, day_of_month))
