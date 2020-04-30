import glob
import json
import os

import exifread
import pytest

from getImageMetadata.metadata import restructure
from getImageMetadata.metadata import add_group
from getImageMetadata.metadata import to_json

from tests.tools.tools import load_raw_test_metadata


@pytest.fixture(params=load_raw_test_metadata())
def raw_metadata(request):
    return request.param


def test_restructure_all_fields_belong_to_groups(raw_metadata):
    """Verify all items have been added to groups
    and that none have been dropped inadvertently"""
    subitem_count = 0
    for (key, value) in restructure(raw_metadata).items():
        if isinstance(value, dict):
            subitem_count += len(value)

    assert len(raw_metadata.items()) == subitem_count


def test_add_group_adds_group():
    assert "c" in add_group({"a": 1, "b": 2}, "c")


def test_add_group_retains_existing_fields():
    assert "a" in add_group({"a": 1, "b": 2}, "c")
    assert "b" in add_group({"a": 1, "b": 2}, "c")


def test_add_group_added_group_is_empty_dict():
    assert add_group({"a": 1, "b": 2}, "c")["c"] == {}


def test_add_group_returns_dict():
    assert isinstance(add_group({"a": 1, "b": 2}, "c"), dict)


def test_to_json_returns_valid_json_string(raw_metadata):
    json.loads(to_json(raw_metadata))
