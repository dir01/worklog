import argparse
import calendar
import csv
import io

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


parser = argparse.ArgumentParser()
parser.add_argument('--url', help='URL of your google spreadsheet',
                    required=True)
parser.add_argument('--week', help='Comma separated list of weekdays',
                    type=week, default='su,mo,tu,we,th')

url = 'https://docs.google.com/spreadsheets/d/1DFXwHLqvjB-IOGYCjBDwTb6NIksW_nxe_rqWLxkZ0uo/export?format=csv'
