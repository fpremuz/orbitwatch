from sqlalchemy.orm import Session
from app.alerts.domain.models import Alert


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: Alert):

        self.db.add(alert)
        return alert