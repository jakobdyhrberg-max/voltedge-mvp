# Voltedge MVP

Voltedge MVP is a FastAPI-based backend system for EV charger telemetry monitoring and incident detection.

## Features

- Receive telemetry data from EV chargers
- Detect incidents automatically
- Generate alerts based on severity
- Store data in MySQL
- REST API with Swagger documentation
- Dockerized setup
- Automated tests with Pytest
- CI pipeline with GitHub Actions
- API security with API key authentication
- Power BI integration for analytics dashboards

---

# Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL
- Docker
- Pytest
- GitHub Actions
- Power BI

---

# Project Structure

```text
voltedge-mvp/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   └── test_main.py
│
├── .github/workflows/
│   └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Running Locally

## Start application

```bash
docker compose up --build
```

API documentation:

```text
http://localhost:8000/docs
```

---

# Running Tests

## Local tests

```bash
docker compose exec api pytest tests
```

---

# CI/CD

GitHub Actions automatically runs tests on every push to the `main` branch.

---

# DevSecOps & Security

## Continuous Integration

The project uses GitHub Actions for automated CI pipelines.
Tests are automatically executed on every push to the `main` branch to ensure application stability and code quality.

## Dockerized Infrastructure

The backend API and database run inside Docker containers using Docker Compose.

This ensures consistent environments across development and testing.

## API Security

Protected endpoints require an API key using the `x-api-key` request header.

Example:

```text
x-api-key: dev-secret-key
```

API secrets are configured through environment variables instead of hardcoded credentials.

## Logging & Monitoring

The system uses structured logging to monitor:

- telemetry ingestion
- incident detection
- alert generation
- unauthorized API access attempts

This supports operational monitoring and troubleshooting.

## Business Intelligence Integration

Power BI connects directly to FastAPI analytics endpoints through authenticated REST API requests.

This enables near real-time dashboard refreshes without manually exporting CSV files.

---

# Example API Endpoints

## Submit telemetry

```http
POST /telemetry
```

## Get chargers

```http
GET /chargers
```

## Get incidents

```http
GET /incidents
```

## Get alerts

```http
GET /alerts
```

## Analytics summary

```http
GET /analytics/summary
```

## Severity analytics

```http
GET /analytics/severity-count
```

---

# Author

Jakob Dyhrberg Adamsen