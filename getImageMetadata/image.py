from io import BytesIO

import exifread
import urllib3


def fetch_image(url: str) -> BytesIO:
    """Downloads an image from a url and returns it as a .read()-able object"""
    http = urllib3.PoolManager()
    return BytesIO(http.request("GET", url).data)


def extract_metadata(image: BytesIO) -> dict:
    """Image must be a file-like object that has a read() method"""
    return exifread.process_file(image)
