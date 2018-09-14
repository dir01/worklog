import argparse
import calendar
import csv
import io
from datetime import datetime, timedelta

import requests

from analyze import get_date_to_timedelta_map_by_dt_to_event_map
from format import Formatter
from ideal_stats import IdealStats
from stats import Stats
from transform import get_dt_to_event_map_by_raw_event_list


def run():
    args = parser.parse_args()
    ideal = IdealStats(hours_per_day=8, work_weekdays=args.week)

    google_csv_url = url
    data = requests.get(google_csv_url).text
    raw_log = list(csv.reader(io.StringIO(data, newline=None)))

    dt_event_map = get_dt_to_event_map_by_raw_event_list(raw_log)
    date_to_timedelta_map = get_date_to_timedelta_map_by_dt_to_event_map(
        dt_event_map)

    stats = Stats(date_to_timedelta_map, start_of_week=args.week[0])

    formatter = Formatter(stats=stats, ideal=ideal)
    print('''Month:\t{fmt.month}\nWeek:\t{fmt.week}\nDay:\t{fmt.day}'''.format(
        fmt=formatter))


def week(week_string):
    mapping = {
        'su': calendar.SUNDAY,
        'mo': calendar.MONDAY,
        'tu': calendar.TUESDAY,
        'we': calendar.WEDNESDAY,
        'th': calendar.THURSDAY,
        'fr': calendar.FRIDAY,
        'sa': calendar.SATURDAY,
    }

    def str_to_weekday(s):
        try:
            return mapping[s[:2].lower()]
        except KeyError:
            raise ValueError

    week_days = tuple(filter(bool, week_string.split(',')))
    if not week_days:
        raise ValueError

    return [
        str_to_weekday(day_of_week_str)
        for day_of_week_str in week_days
        if day_of_week_str
        ]


def holiday(holiday_str):
    if ':' in holiday_str:
        date_str, hours_str = holiday_str.split(':')
    else:
        date_str = holiday_str
        hours_str = '0'
    date = datetime.strptime(date_str, '%d.%m.%y').date()
    return date, timedelta(hours=int(hours_str))


class StoreHoliday(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        result = getattr(namespace, self.dest) or {}
        for k, v in values:
            result[k] = v
        setattr(namespace, self.dest, result)


parser = argparse.ArgumentParser()
parser.add_argument('--url', help='URL of your google spreadsheet',
                    required=True)
parser.add_argument('--week', help='Comma separated list of weekdays',
                    type=week, default='su,mo,tu,we,th')
parser.add_argument('--holiday',
                    help='Special day with less or zero hours, '
                         'e.g: --holiday=09.09.18:3 --holiday=10.09.18 would mean '
                         'that at September, 9th you worked for three hours, '
                         'and at September, 10th you didnt work at all',
                    nargs='*', type=holiday, action=StoreHoliday)
url = 'https://docs.google.com/spreadsheets/d/1DFXwHLqvjB-IOGYCjBDwTb6NIksW_nxe_rqWLxkZ0uo/export?format=csv'
