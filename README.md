# VoltEdge Charger Monitoring MVP

A cloud-native EV charger monitoring MVP built with FastAPI, MySQL, Docker, Power BI, and a simple machine learning model for predictive maintenance analytics.

The system receives telemetry data from EV chargers, stores operational data in a MySQL database, generates incidents and alerts based on charger conditions, performs predictive maintenance analysis, and visualizes operational analytics in Power BI dashboards.

---

## Architecture

Telemetry/API Requests
        ↓
FastAPI Microservice
        ↓
TelemetryAnalysisService + PredictiveMaintenanceService
        ↓
MySQL Operational Database
        ↓
Power BI Dashboard

The solution follows a layered architecture where:

- FastAPI handles telemetry ingestion and API validation
- TelemetryAnalysisService handles operational incident detection
- PredictiveMaintenanceService performs rule-based predictive analytics and machine learning predictions
- MySQL stores telemetry, incidents, alerts, and predictive risk scores
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
| Analytics & Visualization | Power BI |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas |
| Model Persistence | Joblib |
| Language | Python |

---

## Project Structure

voltedge-mvp/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   │
│   └── ml/
│       ├── train_model.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## Running the Project

### Start containers

docker compose up --build

### Stop containers

docker compose down

The solution runs in Docker containers:
- FastAPI API container
- MySQL database container

Swagger documentation is available at:

http://localhost:8000/docs

---

## Database Configuration

The MVP uses MySQL for persistent operational storage.

Connection string:

DATABASE_URL=mysql+pymysql://voltedge_user:voltedge_pass@db:3306/voltedge

The following tables are automatically created:
- telemetry_readings
- chargers
- incidents
- alerts

The incidents table also supports:
- predictive maintenance incidents
- nullable risk_score values for predictive analytics

The database persists data using Docker volumes.

---

## API Security

The telemetry endpoint is protected with a simple API key mechanism as part of the MVP security setup.

The API key is configured through the Docker environment:

API_KEY=dev-secret-key

Requests to protected endpoints must include the following header:

x-api-key: dev-secret-key

This demonstrates a basic DevSecOps principle by avoiding completely open ingestion endpoints. In a production setup, this should be replaced with stronger authentication and secret management such as OAuth2, Azure Key Vault, or managed secrets.

---

## Predictive Maintenance and Machine Learning

The MVP includes a PredictiveMaintenanceService that combines rule-based risk scoring with a simple Logistic Regression machine learning model.

The service evaluates telemetry data such as:
- temperature
- voltage
- current
- power consumption
- charger status
- error codes

Based on the analysis, the system generates predictive maintenance incidents when a charger shows signs of elevated operational risk.

The machine learning model is trained using Scikit-learn and stored with Joblib as:

app/ml/maintenance_model.pkl

Predictive maintenance incidents are stored in the database together with a calculated risk_score, which can later be visualized in Power BI dashboards.

---

## Example Telemetry Request

Example request sent to:

POST /telemetry

Required header:

x-api-key: dev-secret-key

Example payload:

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

---

## Power BI Integration

Power BI connects directly to the MySQL database.

### Connection Settings

Server: localhost:3307
Database: voltedge
Username: voltedge_user
Password: voltedge_pass

The Power BI dashboard visualizes:
- Total telemetry readings
- Total incidents detected
- Faulted chargers
- Critical incidents
- Predictive maintenance alerts
- Average risk score
- Charger status distribution
- Power consumption trends
- Temperature monitoring
- Operational KPIs

The dashboard supports operational monitoring and provides visibility into charger health, incidents, and predictive maintenance risks.

---

## Features

- Telemetry ingestion API
- Persistent MySQL storage
- Incident generation
- Alert management
- Rule-based predictive analytics
- Simple machine learning model
- Predictive maintenance risk scoring
- Operational monitoring dashboards
- Dockerized deployment
- Power BI analytics integration

---

## Authors

VoltEdge MVP Project Team