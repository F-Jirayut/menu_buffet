import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile
from app.config import settings
from fastapi import HTTPException

def get_s3_client():
    try:
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
    except (BotoCoreError, ClientError) as e:
        print(f"S3 client failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"S3 client failed: {str(e)}")

def upload_file_s3(image: UploadFile, path: str) -> None:
    try:
        s3_client = get_s3_client()
        s3_client.upload_fileobj(
            image.file,
            settings.AWS_BUCKET_NAME,
            path,
            ExtraArgs={"ContentType": image.content_type}
        )
    except (BotoCoreError, ClientError) as e:
        print(f"S3 upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")


def generate_presigned_url(key: str, expiration: int = 600) -> str | None:
    try:
        s3_client = get_s3_client()
        return s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': key},
            ExpiresIn=expiration
        )
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to generate presigned URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")
    
def delete_file_s3(path: str) -> None:
    try:
        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=path)
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to delete S3 file: {str(e)}")
        raise HTTPException(status_code=500, detail="S3 delete failed: " + str(e))
