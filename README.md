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

---

# Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL
- Docker
- Pytest
- GitHub Actions

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

---

# Author

Jakob Dyhrberg Adamsen