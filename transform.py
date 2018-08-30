from datetime import datetime
from const import EVENTS


def get_dt_to_event_map_by_raw_event_list(data):
    return {
        datetime.strptime(raw_dt, '%B %d, %Y at %I:%M%p'): {
            'entered': EVENTS.IN,
            'exited': EVENTS.OUT
        }[raw_event]
        for raw_dt, raw_event, *_ in data
    }
