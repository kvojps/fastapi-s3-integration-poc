from fastapi import FastAPI, UploadFile

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
async def upload_file(file: UploadFile):
    return service.upload_file(file)
