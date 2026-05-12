from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID

from app.core.database import get_db
from app.alerts.domain.models import Alert
from app.alerts.api.schemas import AlertResponse

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "/",
    response_model=list[AlertResponse]
)
def get_alerts(
    satellite_id: UUID | None = None,
    db: Session = Depends(get_db),
):

    query = db.query(Alert)

    if satellite_id:

        query = query.filter(
            Alert.satellite_id == satellite_id
        )

    alerts = (
        query
        .order_by(Alert.created_at.desc())
        .all()
    )

    return alerts


@router.get("/stats")
def get_alert_stats(db: Session = Depends(get_db)):

    result = (
        db.query(
            Alert.level,
            func.count(Alert.id)
        )
        .group_by(Alert.level)
        .all()
    )

    return [
        {
            "level": row[0],
            "count": row[1],
        }
        for row in result
    ]