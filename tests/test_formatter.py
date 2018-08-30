from collections import namedtuple
from datetime import timedelta

from format import Formatter

Stats = namedtuple('Stats', ['day', 'week', 'month'])


class TestFormatter(object):
    def test(self):
        formatter = Formatter(
            stats=Stats(
                day=timedelta(hours=8, minutes=13, seconds=40),
                week=timedelta(hours=33, minutes=18, seconds=34),
                month=timedelta(hours=161, minutes=51, seconds=11),
            ),
            ideal=Stats(
                day=timedelta(hours=9),
                week=timedelta(hours=36),
                month=timedelta(hours=162),
            )
        )
        assert formatter.day == '08:13 of 09:00'
        assert formatter.week == '33:18 of 36:00'
        assert formatter.month == '161:51 of 162:00'
