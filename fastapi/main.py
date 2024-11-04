from fastapi import FastAPI, Request
import time
from metrics import register_request_metrics, start_metric_threads

app = FastAPI()

APP_NAME = "fastapi"

# Inicia as threads de métricas ao iniciar o app
start_metric_threads(app_name=APP_NAME)


# Endpoint de exemplo
@app.get("/test")
def test(request: Request):
    start_time = time.time()
    method = request.method
    path = request.url.path

    # Gera a resposta
    status = 200

    # Registra as métricas de contagem e latência
    register_request_metrics(
        app_name=APP_NAME,
        method=method,
        path=path,
        status=status,
        start_time=start_time,
    )

    return {"message": "Hello, world!"}
