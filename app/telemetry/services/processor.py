def process_batch(self, telemetry_points):

    alerts = []

    for point in telemetry_points:

        self.repo.create_batch(telemetry_points)

        generated_alerts = self.limit_engine.evaluate_point(point)

        for alert in generated_alerts:
            self.alert_repo.create(alert)

        alerts.extend(generated_alerts)

    return alerts