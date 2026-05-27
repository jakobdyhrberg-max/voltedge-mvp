from pathlib import Path

import joblib
import pandas as pd


class PredictiveMaintenanceService:
    MODEL_PATH = Path("app/ml/maintenance_model.pkl")
    model = None

    @classmethod
    def load_model(cls):
        if cls.model is None and cls.MODEL_PATH.exists():
            try:
                cls.model = joblib.load(cls.MODEL_PATH)
            except Exception:
                cls.model = None

        return cls.model

    @staticmethod
    def rule_based_risk(data):
        risk_score = 0

        if data.temperature >= 90:
            risk_score += 40
        elif data.temperature >= 70:
            risk_score += 25

        if data.power >= 7:
            risk_score += 20

        if data.voltage < 200 or data.voltage > 250:
            risk_score += 20

        if data.status.upper() == "FAULTED":
            risk_score += 30

        if data.error_code:
            risk_score += 10

        return min(risk_score, 100)

    @classmethod
    def ml_prediction(cls, data):
        model = cls.load_model()

        if model is None:
            return 0

        input_data = pd.DataFrame([{
            "temperature": data.temperature,
            "power": data.power,
            "voltage": data.voltage,
            "current": data.current
        }])

        try:
            prediction = model.predict(input_data)[0]
            return int(prediction)
        except Exception:
            return 0

    @classmethod
    def predict(cls, data):
        rule_score = cls.rule_based_risk(data)
        ml_prediction = cls.ml_prediction(data)

        final_score = rule_score

        if ml_prediction == 1:
            final_score += 20

        final_score = min(final_score, 100)

        if final_score >= 70:
            risk_level = "HIGH"
        elif final_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "ml_prediction": ml_prediction
        }


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

        prediction = PredictiveMaintenanceService.predict(data)

        if prediction["risk_level"] == "HIGH":
            incidents.append({
                "type": "PREDICTIVE_MAINTENANCE",
                "severity": "HIGH",
                "risk_score": prediction["risk_score"],
                "description": (
                    f"Predictive maintenance risk detected. "
                    f"Risk score: {prediction['risk_score']}, "
                    f"ML prediction: {prediction['ml_prediction']}"
                )
            })

        return incidents