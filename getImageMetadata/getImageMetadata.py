from io import BytesIO
import json

import exifread
import urllib3


def lambda_handler(event, context):
    print("Invoked")

    # Parse user request body out from API Gateway proxy request
    request = json.loads(event["body"])

    body = metadata_to_json(get_image_metadata(request["url"]))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": body,
        "isBase64Encoded": False,
    }


def get_image_metadata(url):
    image_bytes = fetch_image_bytes(url)
    image = bytes_to_image(image_bytes)
    return extract_metadata(image)


def fetch_image_bytes(url):
    print(f"Fetching image {url}")
    http = urllib3.PoolManager()
    return http.request("GET", url).data


def bytes_to_image(b):
    print("Building image")
    return BytesIO(b)


def extract_metadata(image):
    print("Parsing metadata")
    return exifread.process_file(image)


def metadata_to_json(metadata):
    def serialize(value):
        if isinstance(value, exifread.classes.IfdTag):
            return value.printable
        else:
            return str(value)

    return json.dumps(metadata, default=serialize, sort_keys=True)
