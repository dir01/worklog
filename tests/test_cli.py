# -*- coding: utf-8 -*-
from datetime import date, timedelta
from io import StringIO
from unittest.mock import patch

from run import parser


class TestCli(object):
    def test_url_is_required(self):
        self.parse_args('', error='arguments are required: --url')

    def test_spreadsheet_url_is_transformed_to_csv_url(self):
        args = self.parse_args('--url=https://docs.google.com/spreadsheets/d/1DFXwHLqvjB-IOGYCtBDwTb6NIksW_nxe_rqWLxkZ0uo/edit#gid=0')
        assert args.url == 'https://docs.google.com/spreadsheets/d/1DFXwHLqvjB-IOGYCtBDwTb6NIksW_nxe_rqWLxkZ0uo/export?format=csv'

    def test_code_is_transformed_to_csv_url(self):
        args = self.parse_args('--url=1DFXwHLqvjB-IOGYCtBDwTb6NIksW_nxe_rqWLxkZ0uo')
        assert args.url == 'https://docs.google.com/spreadsheets/d/1DFXwHLqvjB-IOGYCtBDwTb6NIksW_nxe_rqWLxkZ0uo/export?format=csv'

    def test_week_without_value(self):
        self.parse_args('--week', error='--week: expected one argument')

    def test_week_as_empty_value(self):
        self.parse_args('--week=', error="--week: invalid week value: ''")

    def test_week_with_invalid_values(self):
        self.parse_args('--week=su,mo,tu,wr',
                        error="--week: invalid week value: 'su,mo,tu,wr'")

    def test_holiday(self):
        args = self.parse_args('--url=foo --holiday=09.09.18')
        assert args.holiday == {date(2018, 9, 9): timedelta(0)}

    def test_partial_holiday(self):
        args = self.parse_args('--url=foo --holiday=09.09.18:3')
        assert args.holiday == {date(2018, 9, 9): timedelta(hours=3)}

    def test_multiple_holidays(self):
        args = self.parse_args(
            '--url=foo --holiday=09.09.18:3 --holiday=10.09.18 --holiday=11.09.18')
        assert args.holiday == {
            date(2018, 9, 9): timedelta(hours=3),
            date(2018, 9, 10): timedelta(0),
            date(2018, 9, 11): timedelta(0),
        }

    def test_missing_holiday(self):
        args = self.parse_args('--url=foo --holiday')
        assert args.holiday == {}

    def test_empty_holiday(self):
        self.parse_args('--url=foo --holiday=',
                        error="--holiday: invalid holiday value: ''")

    def test_invalid_holiday(self):
        self.parse_args('--holiday=2018m11,3:14',
                        error="--holiday: invalid holiday value: '2018m11,3:14")

    def parse_args(self, args, error=None):
        result = None
        with patch('sys.stderr', new_callable=StringIO) as stderr:
            try:
                result = parser.parse_args(args.split(' '))
            except SystemExit:
                pass
        if not error:
            assert 'error' not in stderr.getvalue()
        else:
            assert error in stderr.getvalue()
        return result
