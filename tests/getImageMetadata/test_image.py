import pytest

from getImageMetadata.image import fetch_image
from getImageMetadata.image import extract_metadata

from tests.tools.tools import load_test_images


@pytest.fixture(params=load_test_images())
def image(request):
    return request.param


def test_extract_metadata_returns_dict(image):
    assert isinstance(extract_metadata(image), dict)
