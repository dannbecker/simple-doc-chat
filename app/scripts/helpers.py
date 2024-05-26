from config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
import boto3

def s3_connect():
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        print("Houve um erro:", e)
        s3 = None

    return s3


