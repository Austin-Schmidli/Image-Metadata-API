import glob
import os

import exifread


def generate_test_images():
    for file in glob.glob("tests/resources/images/*"):
        path = os.path.abspath(file)
        with open(path, "rb") as f:
            yield f


def load_test_images():
    images = []
    for file in glob.glob("tests/resources/images/*"):
        path = os.path.abspath(file)
        images.append(open(file, "rb"))

    return images


def load_raw_test_metadata():
    """Generates a list of raw metadata from the test images to aid in testing"""
    raw_metadata = []
    for image in generate_test_images():
        raw_metadata.append(exifread.process_file(image))

    return raw_metadata
