import json
import logging

"""Common functionality that most endpoints will likely require"""


def setup_logger() -> logging.Logger:
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s]: %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger()
    logger.info("Initialized logger")
    return logger


def get_event_body(event: dict) -> dict:
    """Parses the incoming request event
    
    API Gateway wraps the original request with additional information
    The original user request is encoded as a json string in the 'body' field.
    """
    return json.loads(event["body"])
