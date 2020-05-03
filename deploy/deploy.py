import aws
from deploy_layer import publish_layer


def deploy(lambda_client):
    # For now I'm just hardcoding the deployments ¯\_(ツ)_/¯

    # common library
    lib_layer_arn = publish_layer(lambda_client, "lib.zip", "image-metadata-lib")

    # getImageMetadata
    with open("getImageMetadata.zip", "rb") as f:
        getImageMetadataZip = f.read()

    print(f"Updating function code for getImageMetadata")
    response = lambda_client.update_function_code(
        FunctionName="getImageMetadata", ZipFile=getImageMetadataZip
    )
    print(response)

    print(f"Updating function configuration for getImageMetadata")
    response = lambda_client.update_function_configuration(
        FunctionName="getImageMetadata", Layers=[lib_layer_arn]
    )
    print(response)


if __name__ == "__main__":
    parser = aws.get_arg_parser()
    args = parser.parse_args()

    client = aws.get_lambda_client(
        args.AWS_ACCESS_KEY_ID, args.AWS_SECRET_ACCESS_KEY, args.AWS_REGION
    )

    deploy(client)
