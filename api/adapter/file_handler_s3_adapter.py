import os
import uuid

from fastapi import UploadFile

from api.port.file_handler import FileHandlerProvider

from api.config.aws_s3 import S3ClientSession
from api.config.dynaconf import settings


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._s3_client = S3ClientSession
        self._bucket_name = settings.AWS_S3_BUCKET_NAME

    def upload(self, file: UploadFile):
        file_uuid = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        s3_object_key = f"{file_uuid}{file_extension}"

        self._s3_client.upload_fileobj(
            file.file, self._bucket_name, s3_object_key)

    def upload_with_presigned_urls(self, file: UploadFile): ...
