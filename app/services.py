class TelemetryAnalysisService:
    @staticmethod
    def analyze(data):
        incidents = []

        if data.status.upper() == "OFFLINE":
            incidents.append({
                "type": "CHARGER_OFFLINE",
                "severity": "HIGH",
                "description": "Charger is offline"
            })

        if data.temperature > 70:
            incidents.append({
                "type": "HIGH_TEMPERATURE",
                "severity": "CRITICAL",
                "description": "Charger temperature exceeds safe threshold"
            })

        if data.error_code:
            incidents.append({
                "type": "ERROR_CODE_DETECTED",
                "severity": "MEDIUM",
                "description": f"Error code detected: {data.error_code}"
            })

        if data.voltage < 200 or data.voltage > 250:
            incidents.append({
                "type": "VOLTAGE_ANOMALY",
                "severity": "MEDIUM",
                "description": "Voltage is outside expected range"
            })

        return incidents