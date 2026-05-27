from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Charger(Base):
    __tablename__ = "chargers"

    id = Column(String(50), primary_key=True, index=True)
    location = Column(String(100))
    status = Column(String(50), default="UNKNOWN")


class TelemetryReading(Base):
    __tablename__ = "telemetry_readings"

    id = Column(Integer, primary_key=True, index=True)
    charger_id = Column(String(50), ForeignKey("chargers.id"))
    voltage = Column(Float)
    current = Column(Float)
    power = Column(Float)
    temperature = Column(Float)
    status = Column(String(50))
    error_code = Column(String(50), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    charger_id = Column(String(50), ForeignKey("chargers.id"))
    incident_type = Column(String(100))
    severity = Column(String(50))
    description = Column(String(255))
    status = Column(String(50), default="OPEN")
    risk_score = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    message = Column(String(255))
    severity = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())