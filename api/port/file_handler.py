from fastapi import UploadFile
from abc import ABC, abstractmethod


class FileHandlerProvider(ABC):

    @abstractmethod
    def upload_file(self, file: UploadFile): ...

    @abstractmethod
    def create_upload_url(self) -> str: ...
