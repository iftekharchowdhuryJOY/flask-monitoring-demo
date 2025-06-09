# Flask Monitoring with Prometheus & Grafana

Real-time monitoring system for Flask applications using Docker, Prometheus, and Grafana.

## Features
- ✅ Track HTTP requests, errors, and response times
- ✅ Monitor CPU/RAM/disk usage
- ✅ Alerting via Slack/Email
- ✅ Dockerized for easy deployment

## Quick Start
```bash
git clone https://github.com/yourusername/flask-monitoring-demo.git
cd flask-monitoring-demo
docker-compose up --build

## Access services:

- Flask App: http://localhost:5000

- Prometheus: http://localhost:9090

- Grafana: http://localhost:3000 (admin/admin)
```

## Step 1: Setting Up the Flask App with Metrics
### 1.1 Instrumenting Flask with Prometheus
First, I added Prometheus metrics to a simple Flask app:

```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
RESPONSE_TIME = Histogram('http_response_time_seconds', 'Response time in seconds')

@app.route('/')
def home():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    
    # Simulate work
    time.sleep(0.2)
    
    # Record response time
    RESPONSE_TIME.observe(time.time() - start_time)
    return "Hello, monitored world!"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}
```

## 1.2 Dockerizing the Flask App
I containerized the app for reproducibility:

```dockerfile
# app/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Step 2: Configuring Prometheus
### 2.1 Prometheus Configuration
I set up prometheus.yml to scrape Flask metrics:

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['flask-app:8000']  # Docker service name
Why This Matters:

scrape_interval: 15s ensures frequent metric collection.

Prometheus auto-discovers targets via Docker networking.

2.2 Adding System Metrics (Node Exporter)
For server monitoring, I added Node Exporter:
# In docker-compose.yml
services:
  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"

Then updated prometheus.yml:
scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```
## Step 3: Visualizing Data in Grafana
### 3.1 Pre-Built Dashboards

I imported these dashboards (Grafana IDs):

1. Node Exporter Full (1860) (CPU/RAM/Disk)

2. HTTP Metrics (13230) (Flask monitoring)

Steps: Go to Grafana → "+" → "Import" → Enter ID. Select Prometheus as the data source.

## 3.2 Custom Dashboard for Flask
### I created a custom dashboard to track:

1. Request rate (rate(http_requests_total[5m]))

2. Error rate (rate(http_requests_total{status=~"5.."}[5m]))

3. Latency (histogram_quantile(0.95, rate(http_response_time_seconds_bucket[5m])))

## Step 4: Setting Up Alerts
## 4.1 Alert Rules in Grafana

I configured alerts for:
1. High error rate (>5% 5xx responses for 5min)
2. Slow responses (p95 latency >1s)

# Example alert rule
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate on {{ $labels.instance }}"
```
## 4.2 Slack Notifications
I integrated Slack using Grafana’s webhook:

Created a Slack incoming webhook. Added it in Grafana → "Alerting" → "Notification channels".

##Step 5: Deployment with Docker Compose
Final docker-compose.yml:

```yaml
version: '3.8'

services:
  flask-app:
    build: ./app
    ports:
      - "5000:5000"
      - "8000:8000"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus:/etc/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    volumes:
      - grafana-storage:/var/lib/grafana
    ports:
      - "3000:3000"

volumes:
  grafana-storage:

```
## Deploy with one command:
```docker-compose up --build -d```

## Pre-Configured Dashboards

1. Application Metrics: HTTP traffic, error rates
2. System Health: CPU, memory, disk usage
3. Business KPIs: Request rates by endpoint

## Alert Examples

- HTTP 5xx errors > 5%
- Response time > 1s (p95)
- Server CPU > 80%



