import pytest

from tests.tools.tools import load_test_images
from img_metadata_lib.image import fetch_image
from img_metadata_lib.image import extract_metadata


@pytest.fixture(params=load_test_images())
def image(request):
    return request.param


def test_extract_metadata_returns_dict(image):
    assert isinstance(extract_metadata(image), dict)
