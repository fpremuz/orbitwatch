from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
def get_alerts(db: Session = Depends(get_db)):

    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return alerts