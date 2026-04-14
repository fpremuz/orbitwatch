from sqlalchemy.orm import Session

from app.telemetry.domain.parameter_models import TelemetryParameter


class ParameterService:

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_parameter(self, satellite_id, name):

        parameter = (
            self.db.query(TelemetryParameter)
            .filter(
                TelemetryParameter.satellite_id == satellite_id,
                TelemetryParameter.name == name,
            )
            .first()
        )

        if parameter:
            return parameter

        # Create parameter dynamically
        parameter = TelemetryParameter(
            satellite_id=satellite_id,
            name=name,
        )

        self.db.add(parameter)
        self.db.flush()  # get ID without commit

        return parameter