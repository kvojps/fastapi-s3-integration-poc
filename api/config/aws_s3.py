import boto3
import logging

from typing import Any

from fastapi import Depends

from botocore.exceptions import ClientError
from botocore.client import BaseClient

from api.config.dynaconf import settings


class S3Config:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._region = settings.AWS_REGION
        self._aws_access_key_id = settings.MKTPLACE_AWS_ACCESS_KEY_ID
        self._aws_secret_access_key = settings.MKTPLACE_AWS_SECRET_ACCESS_KEY

    def s3_client(self) -> BaseClient:
        try:
            s3 = boto3.client(
                's3',
                self._region,
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key
            )
            return s3

        except ClientError as e:
            self._logger.error(f'S3 Client startup error:  {e}')
            raise e
