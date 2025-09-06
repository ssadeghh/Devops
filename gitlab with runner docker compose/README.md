# GitLab with GitLab Runner (Docker Compose Setup)

This repository contains a simple setup to run **GitLab CE** along with **GitLab Runners** using Docker Compose.  
The goal is to have a local GitLab server with different types of runners (Shell and Docker) for CI/CD pipelines.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/gitlab-with-runner.git
cd gitlab-with-runner
```

### 2. Start GitLab and Runner
```bah
docker compose up -d
```

### 3. Access GitLab
- URL: http://localhost:8000
- Default credentials (from docker-compose.yml):
  - Email: youremail@gmail.com
  - Password: Abcd@0123456789

## ⚙️ Docker Compose Configuration
### GitLab Server
- Image: ```docker.arvancloud.ir/gitlab/gitlab-ce:latest```
- Ports: ```8000:8000```
- Volumes:
  - ```./gitlab/config:/etc/gitlab``` → GitLab configuration files
  - ```./gitlab/data:/var/opt/gitlab``` → GitLab application data

### GitLab Runner
- Image: ```gitlab/gitlab-runner:alpine```
- Network Mode: ```host``` (to allow direct communication with Docker and GitLab)
- Volumes:
  - ```/var/run/docker.sock:/var/run/docker.sock``` → Allow runner to run Docker jobs
  - ```./gitlab-runner/config:/etc/gitlab-runner``` → Runner configuration

## 🏃 Registering Runners
After starting the containers, you need to register the runner inside the ```gitlab-runner``` container.

#### Step into the Runner container:

```bash
docker compose exec -it gitlab-runner /bin/bash
```

#### Register the runner:
```bash
gitlab-runner register \
  --url http://localhost:8000 \
  --token <your-registration-token> \
  --docker-volumes /var/run/docker.sock:/var/run/docker.sock \
  --docker-network-mode 'host'
```

Replace ```<your-registration-token>``` with the actual token provided in GitLab project settings.

## 🔧 Runner Types
This setup includes two types of runners:
### 1. Shell Runner
- Executes jobs directly on the host shell.
- Simple and fast, but less isolated.

### 2. Docker Runner
- Runs jobs inside Docker containers.
- Supports isolated builds, dependencies, and custom Docker images.
- Requires ```docker.sock``` to be mounted inside the container.

#### Example ```config.toml```
Located in ```./gitlab-runner/config/config.toml```:
```bash
[[runners]]
  name = "docker-runner"
  url = "http://localhost:8000"
  token = "<your-registration-token>"
  executor = "docker"

  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    network_mode = "host"
    helper_image = "docker.arvancloud.ir/gitlab/gitlab-runner-helper:x86_64-v18.3.1"
```


## 📂 Volumes Overview
| Service       | Host Path                | Container Path         | Purpose                          |
| ------------- | ------------------------ | ---------------------- | -------------------------------- |
| gitlab-server | `./gitlab/config`        | `/etc/gitlab`          | GitLab configuration             |
| gitlab-server | `./gitlab/data`          | `/var/opt/gitlab`      | GitLab data storage              |
| gitlab-runner | `/var/run/docker.sock`   | `/var/run/docker.sock` | Allow Docker-in-Docker execution |
| gitlab-runner | `./gitlab-runner/config` | `/etc/gitlab-runner`   | Runner configuration             |


## ✅ Notes
- GitLab may take a few minutes to start on first run.
- Make sure ports (e.g., 8000) are not in use.
- Use the project settings in GitLab ```(Settings → CI/CD → Runners)``` to manage and verify your runners.