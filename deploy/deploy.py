import aws
from deploy_function import deploy_function
from deploy_layer import publish_layer


def deploy(lambda_client):
    # For now I'm just hardcoding the deployments ¯\_(ツ)_/¯

    # img_metadata_lib common library
    img_metadata_lib_arn = publish_layer(
        lambda_client, "img_metadata_lib_layer.zip", "image-metadata-layer"
    )

    # getImageMetadata
    deploy_function(
        lambda_client,
        "getImageMetadata",
        "getImageMetadata.zip",
        [img_metadata_lib_arn],
    )

    # getMetadataByIFD
    deploy_function(
        lambda_client,
        "getMetadataByIFD",
        "getMetadataByIFD.zip",
        [img_metadata_lib_arn],
    )


if __name__ == "__main__":
    parser = aws.get_arg_parser()
    args = parser.parse_args()

    client = aws.get_lambda_client(
        args.AWS_ACCESS_KEY_ID, args.AWS_SECRET_ACCESS_KEY, args.AWS_REGION
    )

    deploy(client)
