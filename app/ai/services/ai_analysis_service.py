from app.ai.providers.router import AIProviderRouter

class AIAnalysisService:
    def __init__(self):
        self.provider = AIProviderRouter()

    def analyze_telemetry(self, data):
        prompt = f"""
        Analyze satellite telemetry:

        Satellite: {data.satellite_id}
        Temperature: {data.temperature}
        Battery: {data.battery}
        Signal: {data.signal_strength}
        Orbit deviation: {data.orbit_deviation}

        Return anomalies, severity and recommendation.
        """

        raw = self.provider.generate(prompt)

        severity = "low"

        if data.battery < 20 or data.signal_strength < 10:
            severity = "high"
        elif data.orbit_deviation > 0.05:
            severity = "medium"

        return {
            "summary": raw,
            "severity": severity,
            "recommendation": "Monitor system" if severity != "high" else "Immediate intervention required"
        }