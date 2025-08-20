import boto3
from botocore.exceptions import  BotoCoreError, ClientError
from botocore.config import Config
import logging

# ------------------------
# Logging Setup
# ------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------
# Session & Client
# ------------------------
session = boto3.session.Session(region_name="us-east-1")
s3_client = session.client("s3", config=Config(retries={"max_attempts": 3}))

# ------------------------
# Bucket Management
# ------------------------
def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} created successfully")
    except ClientError as e:
        logger.error(f"ClientError: {e.response['Error']['Message']}")
    except BotoCoreError as e:
        logger.error(f"BotoCoreError: {str(e)}")

def delete_bucket(bucket_name):
    try:
        # Ensure bucket is empty before deletion
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
                logger.info(f"Deleted {obj['Key']} from {bucket_name}")

        s3_client.delete_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting bucket: {str(e)}")

# ------------------------
# Object Management
# ------------------------
def upload_file(bucket_name, file_path, key):
    try:
        s3_client.upload_file(file_path, bucket_name, key, ExtraArgs={"Metadata": {"owner": "boto3-demo"}})
        logger.info(f"File {file_path} uploaded to {bucket_name}/{key}")
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")

def download_file(bucket_name, key, dest_path):
    try:
        s3_client.download_file(bucket_name, key, dest_path)
        logger.info(f"File {key} downloaded to {dest_path}")
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")

def delete_file(bucket_name, key):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        logger.info(f"File {key} deleted from {bucket_name}")
    except Exception as e:
        logger.error(f"Delete failed: {str(e)}")


# ------------------------
# Multipart Upload Example
# ------------------------
def multipart_upload(bucket_name, file_path, key):
    try:
        transfer_config = boto3.s3.transfer.TransferConfig(
                multipart_threshold=1024 * 1024 * 5, #5MB
                multipart_chunksize=1024 * 1024 * 5
                )
        s3_client.upload_file(file_path, bucket_name, key, Config=transfer_config)
        logger.info(f"Multipart upload of {file_path} completed")
    except Exception as e:
        logger.error(f"Multipart upload failed: {str(e)}")

# ------------------------
# Versioning
# ------------------------
def list_versions(bucket_name):
    try:
        response = s3_client.list_object_versions(Bucket=bucket_name)
        for version in response.get('Versions', []):
            logger.info(f"Key: {version['Key']} - VersionId: {version['VersionId']} - IsLatest: {version['IsLatest']}")
    except Exception as e:
        logger.error(f"Error listing versions: {str(e)}")

if __name__=="__main__":
    logger.info("S3 utility module loaded. Add test calls here if needed.")
