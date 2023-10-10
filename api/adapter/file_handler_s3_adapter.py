import os
import io
import uuid

from fastapi import UploadFile, HTTPException

from api.port.file_handler import FileHandlerProvider

from api.config.aws_s3 import S3Config
from api.config.dynaconf import settings

from botocore.exceptions import ClientError


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._session = S3Config()
        self._bucket_name = settings.AWS_S3_BUCKET_NAME

    def upload_file(self, file: UploadFile):
        try:
            contents = file.file.read()
            temp_file = io.BytesIO()
            temp_file.write(contents)
            temp_file.seek(0)

            file_uuid = str(uuid.uuid4())
            file_type = os.path.splitext(file.filename)[1]
            s3_object_key = f"{file_uuid}{file_type}"

            self._session.s3_client().upload_fileobj(
                temp_file, self._bucket_name, s3_object_key)
            temp_file.close()

        except ClientError as e:
            error_message = e.response["message"]
            error_code = e.response["Error"]["Code"]
            error_status_code = e.response["ResponseMetadata"]["HTTPStatusCode"]

            self._logger.error(
                f'Upload object failed'
                f'Error code: {error_code}, Error message: {error_message}'
            )

            raise HTTPException(
                status_code=error_status_code, detail=error_message)

    def create_upload_url(self): ...
