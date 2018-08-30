from collections import defaultdict
from datetime import datetime, timedelta

from const import EVENTS


def get_date_to_timedelta_map_by_dt_to_event_map(log):
    """
    :rtype: dict<datetime.date, datetime.timedelta>
    """
    flat_log = sorted(log.items(), key=lambda i: i[0])
    report = defaultdict(timedelta)
    for i, entry in enumerate(flat_log):
        dt, event = entry
        if event != EVENTS.OUT:
            continue
        prev_dt, prev_event = flat_log[i - 1]
        if prev_event != EVENTS.IN:
            continue
        if prev_dt.date() != dt.date():
            continue
        report[dt.date()] += dt - prev_dt
    now = _now()
    last_dt, last_event = flat_log[-1]
    if last_event == EVENTS.IN and last_dt.date() == now.date():
        report[now.date()] += now - last_dt
    return dict(report)


def _now():  # For testability
    return datetime.now()
