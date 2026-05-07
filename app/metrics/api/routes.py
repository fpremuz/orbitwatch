from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db

from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint
from app.satellites.domain.models import Satellite

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):

    total_points = db.query(func.count(TelemetryPoint.id)).scalar()

    total_alerts = db.query(func.count(Alert.id)).scalar()

    critical_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.level == "CRITICAL")
        .scalar()
    )

    total_satellites = db.query(func.count(Satellite.id)).scalar()

    return {
        "total_points": total_points,
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "total_satellites": total_satellites,
    }