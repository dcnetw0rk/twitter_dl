# coding: utf-8

"""
Unit tests for the args module.
"""

import argparse
from datetime import datetime
import pytest
from ..src.args import parse_date, parse_args, parse_file_arg


def test_parse_date_invalid():
    """Ensure that invalid dates fail to parse."""
    with pytest.raises(argparse.ArgumentTypeError, match="Not a valid date: 'test'."):
        assert parse_date('test')


def test_parse_date_valid():
    """Ensure that proper dates parse correctly."""
    assert parse_date('2019-06-27 13:20') == datetime(2019, 6, 27, 13, 20, 0, 0)
    assert parse_date('2019-06-27') == datetime(2019, 6, 27, 0, 0, 0, 0)


def test_parse_args():
    """Ensure that a full list of arguments can get parsed correctly."""
    args = ['-o', 'out', '-f', '[%date%] %filename%.%ext%', '-s', 'large', '-u', 'Twitter']
    parsed = parse_args(args)
    assert parsed.userid == ['Twitter']
    assert parsed.o_userid is True
    assert parsed.output == 'out'
    assert parsed.format == '[%date%] %filename%.%ext%'
    assert parsed.image_size == 'large'


def test_parse_file_arg_basic():
    """Ensure that parse_file_arg works for basic use cases."""
    parsed = parse_file_arg('Twitter')
    assert parsed == ['Twitter']


def test_parse_file_arg_file():
    """Ensure that parse_file_arg works for reading text files."""
    test_file = 'test_args.txt'
    with open(test_file, 'w') as file_descriptor:
        file_descriptor.write('Twitter\nOther\nUser')
    parsed = parse_file_arg('@' + test_file)
    assert parsed == ['Twitter', 'Other', 'User']
