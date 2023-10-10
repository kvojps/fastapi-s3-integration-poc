from fastapi import UploadFile

from api.port.file_handler import FileHandlerProvider


class FileHandlerService:
    def __init__(self, file_handler_provider: FileHandlerProvider) -> None:
        self._file_handler_provider = file_handler_provider

    def upload_file(self, file: UploadFile):
        self._file_handler_provider.upload_file(file)

    def create_upload_url(self) -> str:
        return self._file_handler_provider.create_upload_url()
