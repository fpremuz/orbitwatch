from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import SessionLocal
from app.core.redis import redis_client


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/live")
def liveness_check():

    return {
        "status": "alive",
    }


@router.get("/ready")
def readiness_check():

    db_ok = False
    redis_ok = False

    try:

        with SessionLocal() as db:
            db.execute(text("SELECT 1"))

        db_ok = True

    except Exception:
        db_ok = False

    try:

        redis_client.ping()
        redis_ok = True

    except Exception:
        redis_ok = False

    overall_status = (
        db_ok and redis_ok
    )

    return {
        "status": (
            "ready"
            if overall_status
            else "not_ready"
        ),
        "database": db_ok,
        "redis": redis_ok,
    }