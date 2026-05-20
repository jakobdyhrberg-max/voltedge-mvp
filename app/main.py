import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Charger, TelemetryReading, Incident, Alert
from .schemas import TelemetryCreate
from .services import TelemetryAnalysisService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="VoltEdge Charger Monitoring MVP")


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/telemetry")
def receive_telemetry(data: TelemetryCreate, db: Session = Depends(get_db)):
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
            description=item["description"]
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
def get_chargers(db: Session = Depends(get_db)):
    logger.info("Fetching all chargers")
    return db.query(Charger).all()


@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    logger.info("Fetching all incidents")
    return db.query(Incident).all()


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    logger.info("Fetching all alerts")
    return db.query(Alert).all()