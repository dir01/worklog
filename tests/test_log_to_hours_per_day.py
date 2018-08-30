from unittest.mock import patch
from datetime import datetime, date, timedelta

from const import EVENTS
from analyze import get_date_to_timedelta_map_by_dt_to_event_map

FUT = get_date_to_timedelta_map_by_dt_to_event_map


class TestLogToHoursPerDay(object):
    def test_in_and_out(self):
        result = FUT({
            datetime(2018, 7, 15, hour=8, minute=30): EVENTS.IN,
            datetime(2018, 7, 15, hour=18): EVENTS.OUT
        })
        assert result == {date(2018, 7, 15): timedelta(hours=9, minutes=30)}

    def test_multiple_ins_and_outs(self):
        result = FUT({
            datetime(2018, 7, 15, 8, 30): EVENTS.IN,
            datetime(2018, 7, 15, 13, 00): EVENTS.OUT,
            datetime(2018, 7, 15, 14, 00): EVENTS.IN,
            datetime(2018, 7, 15, 18): EVENTS.OUT
        })
        assert result == {date(2018, 7, 15): timedelta(hours=8, minutes=30)}

    def test_multiple_days(self):
        result = FUT({
            datetime(2018, 7, 15, 8): EVENTS.IN,
            datetime(2018, 7, 15, 18): EVENTS.OUT,
            datetime(2018, 7, 16, 9): EVENTS.IN,
            datetime(2018, 7, 16, 19): EVENTS.OUT
        })
        assert result == {
            date(2018, 7, 15): timedelta(hours=10),
            date(2018, 7, 16): timedelta(hours=10),
        }

    def test_missed_in(self):
        result = FUT({
            datetime(2018, 7, 15, 8): EVENTS.IN,
            datetime(2018, 7, 15, 18): EVENTS.OUT,
            datetime(2018, 7, 14, 8): EVENTS.IN,
            datetime(2018, 7, 14, 18): EVENTS.OUT,
            datetime(2018, 7, 14, 20): EVENTS.OUT,
        })
        assert result == {
            date(2018, 7, 14): timedelta(hours=10),
            date(2018, 7, 15): timedelta(hours=10),
        }

    def test_today(self):
        with patch(
            'analyze._now',
            return_value=datetime(2018, 7, 15, 18, 00)
        ):
            result = FUT({
                datetime(2018, 7, 14, 11, 00): EVENTS.IN,
                datetime(2018, 7, 14, 19, 00): EVENTS.OUT,
                datetime(2018, 7, 15, 11, 00): EVENTS.IN,
            })
            assert result == {
                date(2018, 7, 14): timedelta(hours=8),
                date(2018, 7, 15): timedelta(hours=7),
            }

    def test_today_with_ins_and_outs(self):
        with patch(
            'analyze._now',
            return_value=datetime(2018, 7, 15, 18, 00)
        ):
            result = FUT({
                datetime(2018, 7, 15, 11, 00): EVENTS.IN,
                datetime(2018, 7, 15, 12, 00): EVENTS.OUT,
                datetime(2018, 7, 15, 17, 00): EVENTS.IN,
            })
            assert result == {
                date(2018, 7, 15): timedelta(hours=2),
            }

    def test_today_with_out_event(self):
        with patch(
            'analyze._now',
            return_value=datetime(2018, 7, 15, 18, 00)
        ):
            result = FUT({
                datetime(2018, 7, 15, 11, 00): EVENTS.IN,
                datetime(2018, 7, 15, 12, 00): EVENTS.OUT,
            })
            assert result == {
                date(2018, 7, 15): timedelta(hours=1),
            }




