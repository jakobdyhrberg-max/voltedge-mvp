from dataclasses import dataclass


@dataclass(frozen=True)
class PowerReading:
    value: float


@dataclass(frozen=True)
class TemperatureReading:
    value: float


@dataclass(frozen=True)
class RiskScore:
    value: int