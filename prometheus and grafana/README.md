# 📊 Simple Monitoring with Prometheus & Grafana

This project demonstrates a simple setup for monitoring a Flask web application using **Prometheus** and **Grafana** with **Docker Compose**.
The goal is to create a basic dashboard in Grafana that visualizes metrics collected by Prometheus.


## 📊 Creating a Dashboard in Grafana
1. Log in to Grafana at ```http://localhost:3000```.
2. Go to Connections > Data sources > Add data source.
3. Select Prometheus and set the URL to: ```http://prometheus:9090```.
4. Create a new dashboard and add a panel:
 - For application metrics (if ```/metrics``` is implemented): ```app_requests_total```.
 - For container metrics (via cAdvisor):
    - ```container_cpu_usage_seconds_total```
    - ```container_memory_usage_bytes```

## Project Structure
```bash
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
└── README.md
```

### Access the services
- Flask App → ```http://localhost:5000```
- Prometheus → ```http://localhost:9090```
- Grafana → ```http://localhost:3000``` (default user/pass: ```admin/admin```)
- cAdvisor → ```http://localhost:8080```