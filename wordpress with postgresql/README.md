# WordPress with PostgreSQL, Prometheus & Grafana

This project runs **WordPress** on **PostgreSQL** using the [pg4wp plugin](https://github.com/PostgreSQL-For-Wordpress/postgresql-for-wordpress), and provides monitoring with **Prometheus** and **Grafana**.

---

## 📦 Services

- **Postgres (14)** – Database for WordPress  
- **WordPress (PHP 8.1, Apache)** – Built with PostgreSQL support (via custom Dockerfile)  
- **pg4wp** – WordPress plugin for PostgreSQL support  
- **postgres_exporter** – Exports PostgreSQL metrics for Prometheus  
- **Prometheus** – Scrapes PostgreSQL metrics  
- **Grafana** – Visualizes metrics from Prometheus  

---

## 🚀 Setup

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/wordpress-pg4wp.git
cd wordpress-pg4wp
```

### 2. Build WordPress image
The custom Dockerfile installs PostgreSQL extensions for PHP: 
```bash
vim Dockerfile
```

```bash
FROM wordpress:6.5-php8.1-apache

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && docker-php-ext-install pdo pdo_pgsql pgsql
```

### 3. Start containers
```bash
docker-compose up -d --build
```

### 4. Access services

```bash
WordPress → http://localhost:8080

Prometheus → http://localhost:9090

Grafana → http://localhost:3000
```


## ⚙️ Configuration
### WordPress Database Settings
#### Environment variables 
from ```docker-compose.yml```:
```bash
WORDPRESS_DB_HOST: db:5432
WORDPRESS_DB_NAME: wordpress_db
WORDPRESS_DB_USER: wp_user
WORDPRESS_DB_PASSWORD: wp_pass
```

#### Prometheus
Configuration file ```prometheus.yml```:

```bash
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
```

## 📊 Monitoring
### Example PromQL Queries
- Check PostgreSQL availability:
```bash
pg_up
```
- Number of active connections:
```bash
pg_stat_activity_count
```
- Cache hit ratio:
```bash
(pg_stat_database_blks_hit_total) / (pg_stat_database_blks_hit_total + pg_stat_database_blks_read_total)
```

- CPU usage of exporter:
```bash
process_cpu_seconds_total{job="postgres_exporter"}
```

- Memory usage of exporter:
```bash
process_resident_memory_bytes{job="postgres_exporter"}
```

- Queries waiting:
```bash
pg_stat_activity_waiting
```

## 📂 Project Structure
```bash
wordpress-pg4wp/
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml
└── wp-content/
    ├── db.php
    ├── pg4wp/
    ├── plugins/
    ├── themes/
    └── uploads/
```

## 📝 Notes
- Default Grafana login: admin / admin (you will be prompted to change the password).
- Data is persisted in the ```db_data``` Docker volume.
- Make sure the ```pg4wp``` plugin is activated inside WordPress.

## 🔮 Next Steps
- Add Grafana dashboards for PostgreSQL.
- Secure credentials with Docker secrets.
- Configure persistent storage for WordPress content.

## Example JSON Grafana Dashboard 

```bash
{
  "id": null,
  "title": "PostgreSQL Monitoring",
  "timezone": "browser",
  "schemaVersion": 39,
  "version": 1,
  "refresh": "10s",
  "panels": [
    {
      "type": "stat",
      "title": "Postgres Up",
      "targets": [
        {
          "expr": "pg_up",
          "legendFormat": "Status"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "bool"
        }
      },
      "gridPos": { "x": 0, "y": 0, "w": 4, "h": 4 }
    },
    {
      "type": "graph",
      "title": "Active Connections",
      "targets": [
        {
          "expr": "pg_stat_activity_count",
          "legendFormat": "Connections"
        }
      ],
      "gridPos": { "x": 4, "y": 0, "w": 8, "h": 6 }
    },
    {
      "type": "gauge",
      "title": "Cache Hit Ratio",
      "targets": [
        {
          "expr": "(pg_stat_database_blks_hit_total) / (pg_stat_database_blks_hit_total + pg_stat_database_blks_read_total)",
          "legendFormat": "Hit Ratio"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit",
          "min": 0,
          "max": 1
        }
      },
      "gridPos": { "x": 0, "y": 4, "w": 4, "h": 6 }
    },
    {
      "type": "graph",
      "title": "Exporter CPU Usage",
      "targets": [
        {
          "expr": "rate(process_cpu_seconds_total{job=\"postgres_exporter\"}[1m])",
          "legendFormat": "CPU Seconds"
        }
      ],
      "gridPos": { "x": 0, "y": 10, "w": 6, "h": 6 }
    },
    {
      "type": "graph",
      "title": "Exporter Memory Usage",
      "targets": [
        {
          "expr": "process_resident_memory_bytes{job=\"postgres_exporter\"}",
          "legendFormat": "Memory"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "bytes"
        }
      },
      "gridPos": { "x": 6, "y": 10, "w": 6, "h": 6 }
    },
    {
      "type": "graph",
      "title": "Waiting Queries",
      "targets": [
        {
          "expr": "pg_stat_activity_waiting",
          "legendFormat": "Waiting"
        }
      ],
      "gridPos": { "x": 0, "y": 16, "w": 12, "h": 6 }
    }
  ]
}
```

