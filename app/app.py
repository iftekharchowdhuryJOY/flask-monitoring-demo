from flask import Flask
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import random
import time 

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
CPU_USAGE = Gauge('cpu_usage_percent', 'Simulated CPU Usage')
RESPONSE_TIME = Histogram('http_response_time_seconds', 'Response time in seconds', ['endpoint'])
DB_QUERY_DURATION = Gauge('db_query_duration_ms', 'Database query duration in ms')

@app.route('/')
def home():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    
     # Simulate database query
    time.sleep(random.uniform(0.1, 0.5))
    DB_QUERY_DURATION.set(random.randint(10, 100))
    resp_time = time.time() - start_time
    RESPONSE_TIME.labels(endpoint='/').observe(resp_time)
    return "Hello, monitored world!"

@app.route('/metrics')
def metrics():
    CPU_USAGE.set(42.5)  # Simulate CPU usage (replace with real data)
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    start_http_server(8000)  # Prometheus metrics server
    app.run(host='0.0.0.0', port=5000)