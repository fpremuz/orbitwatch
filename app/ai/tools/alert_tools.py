from sqlalchemy import func

from app.ai.tools.base import Tool
from app.alerts.domain.models import Alert
from app.core.database import SessionLocal


class LatestAlertTool(Tool):

    name = "latest_alert"

    def execute(self):

        db = SessionLocal()

        alert = (
            db.query(Alert)
            .order_by(Alert.created_at.desc())
            .first()
        )

        db.close()

        if alert is None:
            return "No alerts."

        return (
            f"{alert.severity} - "
            f"{alert.message}"
        )


class AlertStatsTool(Tool):

    name = "alert_stats"

    def execute(self):

        db = SessionLocal()

        stats = (
            db.query(
                Alert.severity,
                func.count(Alert.id)
            )
            .group_by(Alert.severity)
            .all()
        )

        db.close()

        if not stats:
            return "No alert statistics."

        return "\n".join(
            f"{severity}: {count}"
            for severity, count in stats
        )