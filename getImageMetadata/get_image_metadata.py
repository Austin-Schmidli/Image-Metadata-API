import json
import logging

from img_metadata_lib import image
from img_metadata_lib import common
from img_metadata_lib import metadata


def lambda_handler(event: dict, context: dict) -> dict:
    logger = common.setup_logger()

    # Parse user request body out from API Gateway proxy request
    request = common.get_event_body(event)

    img = image.fetch_image(request.get("url"))
    img_metadata = image.extract_metadata(img)
    img_metadata = metadata.restructure(img_metadata)

    # Return False if property doesn't exist
    if not request.get("include_thumbnail", False):
        img_metadata = metadata.remove_thumbnail(img_metadata)

    response = metadata.to_json(img_metadata)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": response,
        "isBase64Encoded": False,
    }
