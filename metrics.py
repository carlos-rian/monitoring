from prometheus_client import (
    Gauge,
    generate_latest,
    CollectorRegistry,
    write_to_textfile,
)
import psutil
import time


RUNNING = True

metrics_registry = CollectorRegistry()

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


def update_system_metrics(app_name: str):
    while RUNNING:
        CPU_USAGE.labels(app_name=app_name).set(psutil.cpu_percent())
        MEMORY_USAGE.labels(app_name=app_name).set(psutil.virtual_memory().percent)
        time.sleep(5)


def save_metrics():
    while RUNNING:
        write_to_textfile("metrics.txt", generate_latest(metrics_registry))
        time.sleep(5)  # Intervalo para salvar as métricas
