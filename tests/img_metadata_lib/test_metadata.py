import glob
import json
import os

import exifread
import pytest

from tests.tools.tools import load_raw_test_metadata
from img_metadata_lib.metadata import remove_thumbnail
from img_metadata_lib.metadata import restructure
from img_metadata_lib.metadata import add_IFD
from img_metadata_lib.metadata import to_json


@pytest.fixture(params=load_raw_test_metadata())
def raw_metadata(request):
    return request.param


def test_restructure_all_fields_belong_to_IFDs(raw_metadata):
    """Verify all items have been added to IFDs
    and that none have been dropped inadvertently"""
    subitem_count = 0
    for (key, value) in restructure(raw_metadata).items():
        if isinstance(value, dict):
            subitem_count += len(value)

    assert len(raw_metadata.items()) == subitem_count


def test_add_IFD_adds_IFD():
    assert "c" in add_IFD({"a": 1, "b": 2}, "c")


def test_add_IFD_retains_existing_fields():
    assert "a" in add_IFD({"a": 1, "b": 2}, "c")
    assert "b" in add_IFD({"a": 1, "b": 2}, "c")


def test_add_IFD_added_IFD_is_empty_dict():
    assert add_IFD({"a": 1, "b": 2}, "c")["c"] == {}


def test_add_IFD_returns_dict():
    assert isinstance(add_IFD({"a": 1, "b": 2}, "c"), dict)


def test_to_json_returns_valid_json_string(raw_metadata):
    json.loads(to_json(raw_metadata))


def test_remove_thumbnail_returns_dict():
    assert isinstance(remove_thumbnail({}), dict)


def test_remove_thumbnail_when_no_thumbnail_does_nothing():
    assert remove_thumbnail({"a": 1, "b": 2}) == {"a": 1, "b": 2}


def test_remove_thumbnail_top_level():
    assert remove_thumbnail({"a": 1, "b": 2, "JPEGThumbnail": "data"}) == {
        "a": 1,
        "b": 2,
    }


def test_remove_thumbnail_in_IFD():
    assert remove_thumbnail(
        {"a": 1, "b": 2, "Thumbnail": {"c": 3, "JPEGThumbnail": "data"}}
    ) == {"a": 1, "b": 2, "Thumbnail": {"c": 3}}


def test_remove_thumbnail_in_IFD_doesnt_remove_IFD():
    assert remove_thumbnail(
        {"a": 1, "b": 2, "Thumbnail": {"JPEGThumbnail": "data"}}
    ) == {"a": 1, "b": 2, "Thumbnail": {}}
