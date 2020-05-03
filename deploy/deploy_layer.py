import json

import aws


def publish_layer(lambda_client, zip_path: str, layer_name: str) -> str:
    """Publishes a new lambda layer or new version of an existing lambda layer
    
    Returns the arn (with version) of the created resource."""
    print(f"Publishing lambda layer {layer_name}")

    with open(zip_path, "rb") as f:
        zipfile = f.read()

    response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Content={"ZipFile": zipfile},
        CompatibleRuntimes=["python3.8"],
        LicenseInfo="MIT",
    )

    print(json.dumps(response, indent=4))
    return response["LayerVersionArn"]


if __name__ == "__main__":
    parser = aws.get_arg_parser()
    parser.add_argument("--name", help="Name of layer", type=str)
    parser.add_argument("--zip", help="Path to zip file", type=str)
    args = parser.parse_args()

    client = aws.get_lambda_client(
        args.AWS_ACCESS_KEY_ID, args.AWS_SECRET_ACCESS_KEY, args.AWS_REGION,
    )

    response = publish_layer(client, args.zip, args.name)

    print(response)
