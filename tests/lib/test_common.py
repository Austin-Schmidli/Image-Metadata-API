import logging

import pytest

from lib.common import setup_logger
from lib.common import get_event_body


def test_setup_logger_returns_logger():
    assert isinstance(setup_logger(), logging.Logger)


def test_get_event_body_returns_dict():
    assert isinstance(get_event_body({"body": '{"key": "value"}'}), dict)


def test_get_event_body_returns_body():
    assert get_event_body({"body": '{"key": "value"}'}) == {"key": "value"}
