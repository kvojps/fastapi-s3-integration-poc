from fastapi import UploadFile
from abc import ABC, abstractmethod


class FileHandlerProvider(ABC):

    @abstractmethod
    def upload(self, file: UploadFile): ...

    @abstractmethod
    def upload_with_presigned_urls(self, file: UploadFile): ...
