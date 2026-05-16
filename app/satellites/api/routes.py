from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.satellites.domain.models import (
    Satellite,
)

router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"],
)


@router.get("/overview")
def get_satellites(
    db: Session = Depends(get_db),
):

    satellites = (
        db.query(Satellite)
        .all()
    )

    return satellites