import json
import logging

from getImageMetadata import image
from getImageMetadata import metadata


def lambda_handler(event, context):
    logger = setup_logger()

    # Parse user request body out from API Gateway proxy request
    request = parse_request(event)

    response = metadata_from_url(request["url"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": response,
        "isBase64Encoded": False,
    }


def setup_logger() -> logging.Logger:
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s]: %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger()
    logger.info("Initialized logger")
    return logger


def parse_request(event: dict) -> dict:
    """Parses the incoming request
    
    API Gateway wraps the original request with additional information
    The original user request is encoded as a json string in the 'body' field.
    """
    return json.loads(event["body"])


def metadata_from_url(url) -> dict:
    img = image.fetch_image(url)
    img_metadata = image.extract_metadata(img)
    img_metadata = metadata.restructure(img_metadata)
    return metadata.to_json(img_metadata)
