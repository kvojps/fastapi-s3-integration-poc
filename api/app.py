from fastapi import FastAPI

app = FastAPI(
    title="API - Operações S3",
    version="0.1.0",
    description="API para validação de operações S3 de entrada e saída de arquivos"
)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
