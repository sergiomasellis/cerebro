import os
import boto3
import logging
from botocore.exceptions import NoCredentialsError
from .config import settings

logger = logging.getLogger("cerebro")

def get_s3_client():
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        logger.warning("AWS credentials not configured. S3 upload will fail.")
        return None
    
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_directory_to_s3(local_path: str, bucket_name: str, s3_prefix: str) -> str:
    """
    Uploads a directory to S3 and returns the web URL.
    """
    s3 = get_s3_client()
    if not s3:
        return ""

    if not bucket_name:
        logger.error("S3_BUCKET_NAME not set.")
        return ""

    uploaded_files = 0
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            try:
                content_type = "application/octet-stream"
                if file.endswith(".html"):
                    content_type = "text/html"
                elif file.endswith(".css"):
                    content_type = "text/css"
                elif file.endswith(".js"):
                    content_type = "application/javascript"
                elif file.endswith(".png"):
                    content_type = "image/png"
                elif file.endswith(".jpg") or file.endswith(".jpeg"):
                    content_type = "image/jpeg"
                elif file.endswith(".svg"):
                    content_type = "image/svg+xml"

                s3.upload_file(
                    local_file_path, 
                    bucket_name, 
                    s3_key, 
                    ExtraArgs={'ContentType': content_type}
                )
                uploaded_files += 1
            except FileNotFoundError:
                logger.error(f"The file was not found: {local_file_path}")
            except NoCredentialsError:
                logger.error("Credentials not available")
                return ""
            except Exception as e:
                logger.error(f"Failed to upload {local_file_path}: {e}")

    logger.info(f"Uploaded {uploaded_files} files to s3://{bucket_name}/{s3_prefix}")
    
    # Construct URL (assuming standard S3 website hosting or direct object access)
    # For website hosting: http://bucket-name.s3-website-region.amazonaws.com/prefix
    # For direct access: https://bucket-name.s3.amazonaws.com/prefix/index.html
    return f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_prefix}/index.html"
