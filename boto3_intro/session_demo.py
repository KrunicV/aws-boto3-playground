import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from botocore.config import Config
import logging

#--------------------------
# 1. Logging configuration
#--------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# boto3-specific logging (for less 'noise' use INFO level)
boto3.set_stream_logger('boto3.resources', logging.DEBUG)

#--------------------------
# 2. Sessions
#--------------------------
# Default session (uses ~/.aws/credentials or environment variables)
default_session = boto3.session.Session()

# !!! Do NOT hardcode real credentials !!!
# Custom session with explicit credentials (never commit real ones!)
custom_session = boto3.session.Session(
        aws_access_key_id="FAKEKEY321",
        aws_secret_access_key="FAKESECRET123",
        region_name="us-west-2"
)

logger.info(f"Default session region: {default_session.region_name}")
logger.info(f"Custom session region: {custom_session.region_name}")

#--------------------------
# 3. Config object
#--------------------------
my_config = Config(
        region_name="us-east-1",
        retries={"max_attempts": 3, "mode": "standard",}
)

#--------------------------
# 4. Clients and Resources
#--------------------------
s3_client = default_session.client("s3", config=my_config)
s3_resource = default_session.resource("s3", config=my_config)

# Example with endpoint_url (usefull for LocalStack/testing)
local_s3_client = default_session.client(
        "s3",
        region_name="us-east-1",
        endpoint_url="https://localhost:4566" # Localstack
)


#--------------------------
# 5. Error Handling
#--------------------------
try:
    # Attempt to list buckets
    response = s3_client.list_buckets()
    for bucket in response.get("Buckets", []):
        logger.info(f"Bucket: {bucket['Name']} created on {bucket['CreationDate']}")

except NoCredentialsError:
    logger.error("No AWS credentials found. Please configure your AWS CLI or set env vars.")
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == "NoSuchBucket":
        logger.error("The specified S3 bucket does not exist.")
    elif error_code == "AccessDenied":
        logger.error("You do not have permission to access this bucket.")
    else:
        logger.error(f"Unexpected error: {e.response['Error']['Message']}")
except BotoCoreError as e:
    logger.error(f"BotoCoreError occurred: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")

finally:
    logger.error("S3 operation attempt finished.")
