# pip install -r requeriments.txt
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import logging
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# =========================================================
# CONFIGURAÇÃO DE LOGS (REQUISITO 4 - ESTRUTURA JSON)
# =========================================================

# Configuração básica de log para sair no console (onde o Docker/Promtail lê)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("webhook")

def log_request(endpoint, status, device_id="unknown", message=""):
    """Estrutura de log exigida pelo requisito 4"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoint": endpoint,
        "status": status,
        "device_id": device_id,
        "message": message
    }
    # O logger.info aqui é o que o 'docker logs' e o Loki vão capturar
    logger.info(json.dumps(log_data))


# =========================================================
# CONFIGURAÇÃO DE MÉTRICAS (Prometheus)
# =========================================================

WEBHOOKS_RECEIVED = Counter(
    "jimi_webhooks_received_total",
    "Total de webhooks recebidos",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "jimi_request_latency_ms",
    "Latência das requisições em milissegundos",
    ["endpoint"]
)

HTTP_ERRORS = Counter(
    "jimi_http_errors_total",
    "Total de erros HTTP registrados",
    ["endpoint", "status"]
)


# =========================================================
# VALIDAÇÃO DE PAYLOAD
# =========================================================

SCHEMAS = {
    "telemetry": {"device_id", "timestamp", "payload"},
    "alarms": {"device_id", "alarm_type", "severity"},
    "heartbeat": {"device_id", "status"}
}

def get_json_body():
    return request.get_json(silent=True)

def validate_payload(data: dict | None, schema: str) -> bool:
    if data is None:
        return False
    return SCHEMAS[schema].issubset(data)


# =========================================================
# DECORATOR DE MÉTRICAS
# =========================================================

def track_metrics(endpoint: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            response = func(*args, **kwargs)
            latency = (time.time() - start_time) * 1000
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
            return response
        return wrapper
    return decorator


# =========================================================
# ENDPOINTS
# =========================================================

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "webhook"}), 200


@app.route("/v1/telemetry", methods=["POST"])
@track_metrics("telemetry")
def telemetry():
    data = get_json_body()

    if not validate_payload(data, "telemetry"):
        HTTP_ERRORS.labels(endpoint="telemetry", status="400").inc()
        # Chamada do Log de Erro (Passo 4)
        log_request("/v1/telemetry", 400, message="Invalid Payload")
        return jsonify({"status": "400 error"}), 400

    WEBHOOKS_RECEIVED.labels(endpoint="telemetry").inc()
    # Chamada do Log de Sucesso (Passo 4)
    log_request("/v1/telemetry", 200, data.get("device_id"), "success")

    return jsonify({"status": "ok"}), 200


@app.route("/v1/alarms", methods=["POST"])
@track_metrics("alarms")
def alarms():
    data = get_json_body()

    if not validate_payload(data, "alarms"):
        HTTP_ERRORS.labels(endpoint="alarms", status="400").inc()
        log_request("/v1/alarms", 400, message="Invalid Payload")
        return jsonify({"status": "400 error"}), 400

    WEBHOOKS_RECEIVED.labels(endpoint="alarms").inc()
    log_request("/v1/alarms", 200, data.get("device_id"), "success")

    return jsonify({"status": "ok"}), 200


@app.route("/v1/heartbeat", methods=["POST"])
@track_metrics("heartbeat")
def heartbeat():
    data = get_json_body()

    if not validate_payload(data, "heartbeat"):
        HTTP_ERRORS.labels(endpoint="heartbeat", status="400").inc()
        log_request("/v1/heartbeat", 400, message="Invalid Payload")
        return jsonify({"status": "400 error"}), 400

    WEBHOOKS_RECEIVED.labels(endpoint="heartbeat").inc()
    log_request("/v1/heartbeat", 200, data.get("device_id"), "success")

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)