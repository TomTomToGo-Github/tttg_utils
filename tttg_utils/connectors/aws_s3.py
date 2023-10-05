"""
Description of available python-aws_S3 functions.

Currently only the upload of files to an existing
bucket is possible. This functionality is unused in
the current version of the DB-backup pipeline.
"""


# Load standard python modules
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv


# Load the AWS credentials
load_dotenv()
ACCESS_KEY = os.getenv("AWS_AK")
SECRET_KEY = os.getenv("AWS_SK")
if ACCESS_KEY is None:
    print("No AWS credentials found in .env file")


def upload_to_S3(local_file, bucket, s3_file):
    s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def download_from_s3(bucket, get_file, save_file_as):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3.download_file(bucket, get_file, save_file_as)
        print("Download successful: '{}' was downloaded to '{}'".format(get_file, save_file_as))
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def fetch_object_from_s3_without_downloading(bucket, filename):
    print("      - Connecting to AWS-s3.")
    try:
        s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        print("      - Connection made successfully. Fetching object now")
        fetchedFile = s3.Bucket(bucket).Object(filename).get()
        print("      - Object fetched successfully")
        return fetchedFile
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False