from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CollectorRegistry,
    write_to_textfile,
)
import psutil
import threading
import time


RUNNING = True

# Registry único para todas as métricas
metrics_registry = CollectorRegistry()

# Métricas de requisição com uma etiqueta extra para app_name
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total de requisições HTTP recebidas",
    ["method", "path", "status", "app_name"],
    registry=metrics_registry,
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Tempo de resposta da API",
    ["app_name"],
    registry=metrics_registry,
)

# Métricas de sistema
CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "Uso de CPU em porcentagem",
    ["app_name"],
    registry=metrics_registry,
)
MEMORY_USAGE = Gauge(
    "memory_usage_percent",
    "Uso de memória em porcentagem",
    ["app_name"],
    registry=metrics_registry,
)


# Função para registrar contagem e latência de uma requisição
def register_request_metrics(
    app_name: str, method: str, path: str, status: int, start_time: float
):
    REQUEST_COUNT.labels(
        method=method, path=path, status=status, app_name=app_name
    ).inc()
    REQUEST_LATENCY.labels(app_name=app_name).observe(time.time() - start_time)


# Função para atualizar métricas de sistema
def update_system_metrics(app_name: str):
    while RUNNING:
        CPU_USAGE.labels(app_name=app_name).set(psutil.cpu_percent())
        MEMORY_USAGE.labels(app_name=app_name).set(psutil.virtual_memory().percent)
        time.sleep(5)  # Intervalo de atualização das métricas do sistema


# Função para salvar todas as métricas em um único arquivo
def save_metrics():
    while RUNNING:
        write_to_textfile("metrics.txt", generate_latest(metrics_registry))
        time.sleep(5)  # Intervalo para salvar as métricas


# Inicia as threads para monitoramento de sistema e salvamento de métricas
def start_metric_threads(app_name: str):
    t1 = threading.Thread(target=save_metrics, daemon=True).start()
    t2 = threading.Thread(
        target=update_system_metrics, args=(app_name,), daemon=True
    ).start()

    return t1, t2
