from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total requests to this app")

@app.route("/")
def hello():
    REQUEST_COUNT.inc()
    return "Hello, Prometheus!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)