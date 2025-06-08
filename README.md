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

## Pre-Configured Dashboards

1. Application Metrics: HTTP traffic, error rates
2. System Health: CPU, memory, disk usage
3. Business KPIs: Request rates by endpoint

## Alert Examples

- HTTP 5xx errors > 5%
- Response time > 1s (p95)
- Server CPU > 80%
