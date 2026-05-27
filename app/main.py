import logging
import os

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy import func

import pandas as pd

from .database import Base, engine, get_db
from .models import Charger, TelemetryReading, Incident, Alert
from .schemas import TelemetryCreate
from .services import TelemetryAnalysisService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY", "dev-secret-key")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        logger.warning("Unauthorized API access attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return True


Base.metadata.create_all(bind=engine)

app = FastAPI(title="VoltEdge Charger Monitoring MVP")


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/telemetry")
def receive_telemetry(
    data: TelemetryCreate,
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info(f"Telemetry received from charger {data.charger_id}")

    charger = db.query(Charger).filter(Charger.id == data.charger_id).first()

    if not charger:
        logger.info(f"Creating new charger record: {data.charger_id}")
        charger = Charger(
            id=data.charger_id,
            location=data.location,
            status=data.status
        )
        db.add(charger)
    else:
        logger.info(f"Updating charger status: {data.charger_id} -> {data.status}")
        charger.status = data.status

    reading = TelemetryReading(
        charger_id=data.charger_id,
        voltage=data.voltage,
        current=data.current,
        power=data.power,
        temperature=data.temperature,
        status=data.status,
        error_code=data.error_code
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    logger.info(f"Telemetry reading saved with id {reading.id}")

    detected_incidents = TelemetryAnalysisService.analyze(data)
    created_incidents = []

    for item in detected_incidents:
        logger.warning(
            f"Incident detected for charger {data.charger_id}: "
            f"{item['type']} with severity {item['severity']}"
        )

        incident = Incident(
            charger_id=data.charger_id,
            incident_type=item["type"],
            severity=item["severity"],
            description=item["description"],
            risk_score=item.get("risk_score"),
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        logger.warning(f"Incident created with id {incident.id}")

        alert = Alert(
            incident_id=incident.id,
            message=f"{item['severity']} alert for charger {data.charger_id}: {item['description']}",
            severity=item["severity"]
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        logger.warning(f"Alert created with id {alert.id}")

        created_incidents.append({
            "incident_id": incident.id,
            "type": incident.incident_type,
            "severity": incident.severity
        })

    logger.info(
        f"Telemetry processing completed for charger {data.charger_id}. "
        f"Incidents created: {len(created_incidents)}"
    )

    return {
        "message": "Telemetry received",
        "reading_id": reading.id,
        "incidents_created": created_incidents
    }


@app.get("/chargers")
def get_chargers(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Fetching all chargers")
    return db.query(Charger).all()


@app.get("/incidents")
def get_incidents(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Fetching all incidents")
    return db.query(Incident).all()


@app.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Fetching all alerts")
    return db.query(Alert).all()


@app.get("/analytics/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Fetching analytics summary")

    total_chargers = db.query(Charger).count()
    total_readings = db.query(TelemetryReading).count()
    total_incidents = db.query(Incident).count()
    total_alerts = db.query(Alert).count()
    open_incidents = (
        db.query(Incident)
        .filter(Incident.status == "OPEN")
        .count()
    )

    return {
        "total_chargers": total_chargers,
        "total_telemetry_readings": total_readings,
        "total_incidents": total_incidents,
        "total_alerts": total_alerts,
        "open_incidents": open_incidents
    }


@app.get("/analytics/severity-count")
def get_incidents_by_severity(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Fetching incident count by severity")

    results = (
        db.query(
            Incident.severity,
            func.count(Incident.id)
        )
        .group_by(Incident.severity)
        .all()
    )

    return [
        {
            "severity": severity,
            "count": count
        }
        for severity, count in results
    ]


@app.get("/export/incidents")
def export_incidents(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Exporting incidents to CSV")

    incidents = db.query(Incident).all()

    data = []

    for incident in incidents:
        data.append({
            "id": incident.id,
            "charger_id": incident.charger_id,
            "incident_type": incident.incident_type,
            "severity": incident.severity,
            "description": incident.description,
            "status": incident.status,
            "created_at": incident.created_at
        })

    df = pd.DataFrame(data)

    file_path = "incidents_export.csv"

    df.to_csv(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type="text/csv"
    )


@app.get("/export/alerts")
def export_alerts(
    db: Session = Depends(get_db),
    api_key: bool = Depends(verify_api_key)
):
    logger.info("Exporting alerts to CSV")

    alerts = db.query(Alert).all()

    data = []

    for alert in alerts:
        data.append({
            "id": alert.id,
            "incident_id": alert.incident_id,
            "message": alert.message,
            "severity": alert.severity,
            "created_at": alert.created_at
        })

    df = pd.DataFrame(data)

    file_path = "alerts_export.csv"

    df.to_csv(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type="text/csv"
    )