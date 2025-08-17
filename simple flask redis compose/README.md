# Simple Flask Web Service with Redis

This project demonstrates how to set up a simple web service using **Flask** that communicates with **Redis**. The project uses **Docker** and **Docker Compose** to containerize the application and manage multiple services.

## Project Overview

- **Flask App**: A simple Python web application.
- **Redis**: An in-memory data store used for caching or messaging.
- **Docker**: Containerizes the Flask application.
- **Docker Compose**: Orchestrates the Flask app and Redis service.

## Prerequisites

Make sure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup Instructions

1. **Create a Dockerfile for the Flask app**  
   This Dockerfile will build the Flask application image.

2. **Write a `docker-compose.yml` file**  
   Define both the Flask app and Redis services and configure them to communicate with each other.

3. **Start the services**  
   ```bash
   docker compose up --build

4. **Access the Flask app**  
   The app will typically be available at http://localhost:5000

## Project Structure
    ```bash
    .
    ├── app/
    │   ├── Dockerfile
    │   ├── app.py
    │   └── requirements.txt
    ├── docker-compose.yml
    └── README.md
    
#### Notes
- Ensure the Flask app connects to Redis using the service name defined in docker-compose.yml (e.g., redis).
- You can stop the services with:
    ```bash
    docker compose down
