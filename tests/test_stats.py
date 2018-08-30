from datetime import timedelta, date
from unittest.mock import patch

from stats import Stats


def get_stats(*a, **k):
    return Stats(*a, **k)


"""
Just for reference:

    August 2018       
Su Mo Tu We Th Fr Sa  
          1  2  3  4  
 5  6  7  8  9 10 11  
12 13 14 15 16 17 18  
19 20 21 22 23 24 25  
26 27 28 29 30 31     
"""


class TestStats(object):
    def test_today(self):
        stats = get_stats({
            date(2018, 7, 15): timedelta(hours=8)
        })
        with self.patch_today(date(2018, 7, 15)):
            assert stats.day == timedelta(hours=8)

    def test_week(self):
        stats = get_stats({
            date(2018, 8, 5): timedelta(hours=10),
            date(2018, 8, 6): timedelta(hours=10),
            date(2018, 8, 7): timedelta(hours=10),
            date(2018, 8, 8): timedelta(hours=10),
        })
        with self.patch_today(date(2018, 8, 8)):
            assert stats.week == timedelta(hours=40)

    def test_month(self):
        stats = get_stats({
            date(2018, 8, 3): timedelta(hours=10),
            date(2018, 8, 4): timedelta(hours=10),
        })
        with self.patch_today(date(2018, 8, 8)):
            assert stats.month == timedelta(hours=20)

    def patch_today(self, fake_today):
        return patch('stats.today', return_value=fake_today)
