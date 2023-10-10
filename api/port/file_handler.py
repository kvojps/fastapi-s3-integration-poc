from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from abc import ABC, abstractmethod


class FileHandlerProvider(ABC):

    @abstractmethod
    def upload_file(self, file: UploadFile) -> None: ...

    @abstractmethod
    def create_upload_url(self) -> str: ...

    @abstractmethod
    def download_file(self, file_name: str) -> StreamingResponse: ...
