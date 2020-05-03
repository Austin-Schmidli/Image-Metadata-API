import json
import logging

from img_metadata_lib import image
from img_metadata_lib import common
from img_metadata_lib import metadata


def lambda_handler(event: dict, context: dict) -> dict:
    logger = common.setup_logger()

    # Parse user request body out from API Gateway proxy request
    request = common.get_event_body(event)

    response = metadata_from_url(request["url"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": response,
        "isBase64Encoded": False,
    }


def metadata_from_url(url: str) -> dict:
    img = image.fetch_image(url)
    img_metadata = image.extract_metadata(img)
    img_metadata = metadata.restructure(img_metadata)
    return metadata.to_json(img_metadata)
