import argparse

import boto3

"""Helper module to assist in AWS deployments"""


def get_lambda_client(aws_access_key_id, aws_secret_access_key):
    return boto3.client(
        "lambda",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


def get_arg_parser():
    """Parser to parse out AWS Secrets from command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--AWS_ACCESS_KEY_ID", help="AWS Access Key ID", type=str)
    parser.add_argument(
        "--AWS_SECRET_ACCESS_KEY", help="AWS Secret Access Key", type=str
    )

    return parser
