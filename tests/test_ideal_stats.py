from calendar import SUNDAY, MONDAY, TUESDAY, WEDNESDAY
from datetime import date, timedelta
from unittest.mock import patch

from ideal_stats import IdealStats


def patch_today(day_of_month, month_number=8):
    return patch('ideal_stats.today',
                 return_value=date(2018, month_number, day_of_month))


class TestIdealStats(object):
    """ August 2018
    Su Mo Tu We Th Fr Sa
              1  2  3  4
     5  6  7  8  9 10 11
    12 13 14 15 16 17 18
    19 20 21 22 23 24 25
    26 27 28 29 30 31"""

    stats = IdealStats(
        hours_per_day=9,
        work_weekdays=[SUNDAY, MONDAY, TUESDAY, WEDNESDAY]
    )

    def test_day(self):
        assert self.stats.day == timedelta(hours=9)

    def test_week_at_sunday(self):
        with patch_today(12):
            assert self.stats.week == timedelta(hours=9)

    def test_week_at_wednsday(self):
        with patch_today(14):
            assert self.stats.week == timedelta(hours=3 * 9)

    def test_week_at_friday(self):
        with patch_today(17):
            assert self.stats.week == timedelta(hours=4 * 9)

    def test_month_at_first_week(self):
        with patch_today(4):
            assert self.stats.month == timedelta(hours=1 * 9)

    def test_month_at_the_middle(self):
        with patch_today(15):
            assert self.stats.month == timedelta(hours=9 * 9)

    def test_month_at_the_end(self):
        with patch_today(31):
            assert self.stats.month == timedelta(hours=17 * 9)


def test_holidays():
    """   September 2018
    Su Mo Tu We Th Fr Sa
                       1
     2  3  4  5  6  7  8
     9 10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30"""

    stats = IdealStats(
        hours_per_day=8,
        work_weekdays=[SUNDAY, MONDAY, TUESDAY, WEDNESDAY],
        holidays={
            date(2018, 9, 9): timedelta(hours=4),
            date(2018, 9, 10): timedelta(0),
            date(2018, 9, 11): timedelta(0),
        }
    )
    with patch_today(14, 9):
        assert stats.month == timedelta(hours=5 * 8 + 4)
