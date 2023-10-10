from fastapi import UploadFile, status, HTTPException
from fastapi.responses import StreamingResponse

from api.ports.file_handler import FileHandlerProvider


class FileHandlerService:
    def __init__(self, file_handler_provider: FileHandlerProvider):
        self._file_handler_provider = file_handler_provider

    def upload_file(self, file: UploadFile) -> None:
        self._file_handler_provider.upload_file(file)

    def create_upload_url(self) -> str:
        return self._file_handler_provider.create_upload_url()

    def download_file(self, file_name: str) -> StreamingResponse:
        return self._file_handler_provider.download_file(file_name)
