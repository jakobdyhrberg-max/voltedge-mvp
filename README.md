# VoltEdge Charger Monitoring MVP

A cloud-native EV charger monitoring MVP built with FastAPI, MySQL, Docker, and Power BI.

The system receives telemetry data from EV chargers, stores operational data in a MySQL database, generates incidents and alerts based on charger conditions, and visualizes operational analytics in Power BI dashboards.

---

## Architecture

```text
Telemetry/API Requests
        ↓
FastAPI Microservice
        ↓
MySQL Operational Database
        ↓
Power BI Dashboard
```

The solution follows a layered architecture where:

- FastAPI handles telemetry ingestion and business logic
- MySQL stores operational telemetry, incidents, and alerts
- Docker containerizes the application and database
- Power BI provides analytics and operational monitoring dashboards

---

## Tech Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Containerization | Docker |
| Analytics | Power BI |
| Language | Python |

---

## Project Structure

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
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Running the Project

### Start containers

```bash
docker compose up --build
```

### Stop containers

```bash
docker compose down
```

The solution runs in Docker containers:
- FastAPI API container
- MySQL database container

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

## Database Configuration

The MVP uses MySQL for persistent operational storage.

Connection string:

```env
DATABASE_URL=mysql+pymysql://voltedge_user:voltedge_pass@db:3306/voltedge
```

The following tables are automatically created:
- telemetry_readings
- chargers
- incidents
- alerts

The database persists data using Docker volumes.

---

## Example Telemetry Request

Example request sent to:

```text
POST /telemetry
```

```json
{
  "charger_id": "CH-001",
  "location": "Copenhagen",
  "voltage": 230,
  "current": 16,
  "power": 3.7,
  "temperature": 45,
  "status": "AVAILABLE",
  "error_code": null
}
```

---

## Power BI Integration

Power BI connects directly to the MySQL database.

### Connection Settings

```text
Server: localhost:3307
Database: voltedge
Username: voltedge_user
Password: voltedge_pass
```

The Power BI dashboard visualizes:
- Charger status distribution
- Telemetry trends
- Temperature monitoring
- Incident severity
- Operational KPIs
- Charger availability

---

## Features

- Telemetry ingestion API
- Persistent MySQL storage
- Incident generation
- Alert management
- Operational monitoring dashboards
- Dockerized deployment
- Power BI analytics integration

---


## Authors

VoltEdge MVP Project Team