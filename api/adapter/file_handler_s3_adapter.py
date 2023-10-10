import os
import io
import uuid
import logging

from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse

from api.port.file_handler import FileHandlerProvider

from api.config.aws_s3 import S3Config
from api.config.dynaconf import settings

from botocore.exceptions import ClientError  # type:ignore


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._session = S3Config()
        self._bucket_name = settings.AWS_S3_BUCKET_NAME

    def upload_file(self, file: UploadFile) -> None:
        try:
            if file.filename:
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
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Filename not found")

        except ClientError as e:
            self._handle_upload_exception(e)

    def create_upload_url(self) -> str:
        try:
            upload_url = self._session.s3_client().generate_presigned_url(
                'put_object',
                Params={'Bucket': self._bucket_name, 'Key': str(uuid.uuid4())},
                ExpiresIn=3600)
            if not upload_url:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY, detail="Its not possible create a upload url")

        except ClientError as e:
            self._handle_upload_exception(e)

        return upload_url

    def download_file(self, file_name: str) -> StreamingResponse:
        try:
            response = self._session.s3_client().get_object(
                Bucket=self._bucket_name, Key=file_name)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="File not found!")

            headers = {
                "Content-Disposition": f"attachment; filename={file_name}"}

        except ClientError as e:
            self._handle_download_exception()

        return StreamingResponse(content=response['Body'], headers=headers, status_code=status.HTTP_200_OK)

    def _handle_upload_exception(self, error: ClientError) -> None:
        error_message = error.response["message"]
        error_code = error.response["Error"]["Code"]
        error_status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]

        self._logger.error(
            f'Upload object failed'
            f'Error code: {error_code}, Error message: {error_message}'
        )

        raise HTTPException(
            status_code=error_status_code, detail=error_message)

    def _handle_download_exception(self) -> None:
        self._logger.error(
            f'Download object failed'
            f'Error code: {status.HTTP_404_NOT_FOUND}'
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Download object failed")
