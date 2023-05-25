import boto3
from botocore.client import Config

from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_ENDPOINT_URL,
    AWS_S3_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)


def get_presigned_link(name: str):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME,
    )
    s3 = session.client("s3", endpoint_url=AWS_S3_ENDPOINT_URL, config=Config(signature_version="s3v4"))

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": AWS_STORAGE_BUCKET_NAME, "Key": name},
        ExpiresIn=100,
    )

    return presigned_url
