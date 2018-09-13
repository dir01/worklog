# -*- coding: utf-8 -*-
from io import StringIO
from unittest.mock import patch

from run import parser


class TestCli(object):
    def test_url_is_required(self):
        self.assert_parser_error('', 'arguments are required: --url')

    def test_week_without_value(self):
        self.assert_parser_error('--week', '--week: expected one argument')

    def test_week_as_empty_value(self):
        self.assert_parser_error('--week=', "--week: invalid week value: ''")

    def test_week_with_invalid_values(self):
        self.assert_parser_error('--week=su,mo,tu,wr',
                                 "--week: invalid week value: 'su,mo,tu,wr'")

    def test_correct_args(self):
        self.assert_parser_error('--url=somevalidurl --week=su,mo,tu,we,th',
                                 None)

    def assert_parser_error(self, args, error):
        with patch('sys.stderr', new_callable=StringIO) as stderr:
            try:
                parser.parse_args(args.split(' '))
            except SystemExit:
                pass
        if not error:
            assert 'error' not in stderr.getvalue()
        else:
            assert error in stderr.getvalue()
