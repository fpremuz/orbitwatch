from sqlalchemy import select

from app.alerts.domain.models import Alert
from app.core.database import SessionLocal


class AlertTools:

    def get_recent_alerts(self):

        db = SessionLocal()

        try:

            alerts = (
                db.execute(
                    select(Alert)
                    .order_by(Alert.created_at.desc())
                    .limit(10)
                )
                .scalars()
                .all()
            )

            result = []

            for alert in alerts:

                result.append(
                    {
                        "satellite": str(alert.satellite_id),
                        "severity": alert.severity,
                        "parameter": alert.parameter_name,
                        "value": alert.current_value,
                    }
                )

            return result

        finally:
            db.close()