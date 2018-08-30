from datetime import datetime

from transform import get_dt_to_event_map_by_raw_event_list
from const import EVENTS


def test_transform():
    data = [
        ['July 15, 2018 at 08:23AM', 'entered', ''],
        ['July 15, 2018 at 09:43PM', 'exited', ''],
    ]
    result = get_dt_to_event_map_by_raw_event_list(data)
    assert result == {
        datetime(2018, 7, 15, 8, 23): EVENTS.IN,
        datetime(2018, 7, 15, 21, 43): EVENTS.OUT,
    }
