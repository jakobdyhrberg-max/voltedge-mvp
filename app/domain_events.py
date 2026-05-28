from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TelemetryReceived:
    charger_id: str
    timestamp: datetime


@dataclass(frozen=True)
class AnomalyDetected:
    charger_id: str
    anomaly_type: str
    severity: str
    timestamp: datetime


@dataclass(frozen=True)
class IncidentCreated:
    charger_id: str
    incident_type: str
    severity: str
    timestamp: datetime


@dataclass(frozen=True)
class AlertCreated:
    charger_id: str
    message: str
    severity: str
    timestamp: datetime