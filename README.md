# Devops
https://github.com/PostgreSQL-For-Wordpress/postgresql-for-wordpress

edit ```docker-compose.yml```:
```bash
services:
  db:
    image: postgres:14
    container_name: wp_postgres
    restart: always
    environment:
      POSTGRES_DB: wordpress_db
      POSTGRES_USER: wp_user
      POSTGRES_PASSWORD: wp_pass
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U wp_user"]
      interval: 5s
      retries: 10

  wordpress:
    build: .
    container_name: wp_app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:5432
      WORDPRESS_DB_NAME: wordpress_db
      WORDPRESS_DB_USER: wp_user
      WORDPRESS_DB_PASSWORD: wp_pass
    volumes:
      - ./wp-content:/var/www/html/wp-content
      - ./pg4wp/db.php:/var/www/html/wp-content/db.php

  postgres_exporter:
    image: prometheuscommunity/postgres-exporter:latest
    container_name: postgres_exporter
    environment:
      DATA_SOURCE_NAME: "postgresql://wp_user:wp_pass@db:5432/wordpress_db?sslmode=disable"
    ports:
      - "9187:9187"
    depends_on:
      - db

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - postgres_exporter

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  db_data:
```

edit ```Dockerfile```:
```bash
FROM wordpress:6.5-php8.1-apache

# ﻦﺼﺑ PostgreSQL PHP extension
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && docker-php-ext-install pdo pdo_pgsql pgsql
```

create ```prometheus.yml``` in root dir(wordpress-pg4wp):
```bash
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
```


in ```wp-content```:
```bash
ls wp-content/

db.php  index.php  pg4wp  plugins  themes  uploads
```

```bash
ls wp-content/plugins/
akismet  hello.php  index.php  pg4wp
```
