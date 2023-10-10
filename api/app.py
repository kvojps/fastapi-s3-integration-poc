from fastapi import FastAPI, UploadFile, status
from fastapi.responses import StreamingResponse

from api.service.file_handler import FileHandlerService

from api.adapter.file_handler_s3_adapter import FileHandlerS3Adapter

app = FastAPI(
    title="API - Operações S3",
    version="0.1.0",
    description="API para validação de operações S3 de entrada e saída de arquivos"
)

adapter = FileHandlerS3Adapter()
service = FileHandlerService(adapter)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
def upload_file(file: UploadFile, status_code=status.HTTP_204_NO_CONTENT):
    service.upload_file(file)


@app.get("/upload/url")
def create_upload_url():
    return service.create_upload_url()


@app.get("/download/{file_name}")
def download_file(file_name: str) -> StreamingResponse:
    return service.download_file(file_name)
