# Nexus Repository with Nginx SSL Termination

This project sets up a private **Nexus Repository** server using Docker Compose, with **Nginx** as a reverse proxy performing **SSL termination**. It is intended for **testing and development environments**.

---

## Project Structure

```bash
nexus/
├── certs/
│ ├── certificate.crt # Self-signed SSL certificate
│ ├── private.key # Private key for SSL
│ └── openssl-registry.conf # OpenSSL configuration for certificate generation
├── docker-compose.yml # Docker Compose configuration for Nexus and Nginx
└── registry.conf # Nginx configuration for SSL termination and proxying
```


---

## Services

### Nexus

- **Image**: `sonatype/nexus3`
- **Ports**: 
  - `8081` (UI)
  - `5000` (Docker registry)
- **Volumes**: Persistent storage at `/nexus-data`
- **Environment**: JVM memory configuration for Nexus

### Nginx

- **Image**: `nginx:latest`
- **Ports**: 
  - `80` (HTTP, redirect to HTTPS)
  - `443` (HTTPS)
- **Volumes**: 
  - Nginx configuration (`registry.conf`)
  - SSL certificates (`certs/`)

Nginx is configured to:

1. Redirect all HTTP traffic to HTTPS.
2. Terminate SSL connections using the provided self-signed certificate.
3. Proxy requests:
   - `/ui/` → Nexus UI (`8081`)
   - `/v2/` → Nexus Docker registry (`5000`)

---

## SSL Configuration

A **self-signed certificate** is used for testing purposes.  

### Generating Certificate

The certificate and key are generated using `openssl` with the configuration file `certs/openssl-registry.conf`:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout private.key \
    -out certificate.crt \
    -config openssl-registry.conf
```

- ```CN```: registry.sadegh.com
- ```SAN```: DNS:registry.sadegh.com

### Trusting Self-Signed Certificate
To avoid SSL errors when using Docker clients:

```bash
sudo cp certs/certificate.crt /usr/local/share/ca-certificates/registry.crt
sudo update-ca-certificates
sudo systemctl restart docker
```
Now, you can log in to the registry without SSL errors:
```bash
docker login https://registry.sadegh.com
```

### Docker Compose
```docker-compose.yml``` text:
```bash
version: '3.3'
services:
  nexus:
    image: sonatype/nexus3
    container_name: nexus
    ports:
      - "8081:8081"
      - "5000:5000"
    volumes:
      - nexus-data:/nexus-data
    environment:
      - INSTALL4J_ADD_VM_PARAMS=-Xms1200m -Xmx1200m -XX:MaxDirectMemorySize=2g -Djava.util.prefs.userRoot=/nexus-data/javaprefs
    networks:
      - nexus-network
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./registry.conf:/etc/nginx/conf.d/registry.conf
      - ./certs/:/etc/ssl/
    networks:
      - nexus-network
volumes:
  nexus-data:
    driver: local
networks:
  nexus-network:
    driver: bridge
```

### Nginx Configuration (```registry.conf```)

```bash
server {
    listen 80;
    server_name registry.sadegh.com;
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name registry.sadegh.com;

    ssl_certificate /etc/ssl/certificate.crt;
    ssl_certificate_key /etc/ssl/private.key;

    client_max_body_size 1G;

    location /ui/ {
        proxy_pass http://nexus:8081/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /v2/ {
        proxy_pass http://nexus:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Usage
1. Start services:
```bash
docker-compose up -d
```

2. Access Nexus UI:

```bash
https://registry.sadegh.com/ui/
```

3. Docker login:
```bash
docker login https://registry.sadegh.com
```

## Notes
- This setup uses self-signed certificates suitable only for testing or internal development.

- For production, use CA-signed certificates.

- SSL termination is handled at Nginx, so Nexus itself runs without SSL.