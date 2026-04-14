from sqlalchemy.orm import Session
from collections import defaultdict

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
    
    def get_or_create_parameters_bulk(self, satellite_id, parameter_names: set[str]):

        # 1️⃣ Fetch existing parameters in ONE query
        existing = (
            self.db.query(TelemetryParameter)
            .filter(
                TelemetryParameter.satellite_id == satellite_id,
                TelemetryParameter.name.in_(parameter_names),
            )
            .all()
        )

        existing_map = {p.name: p for p in existing}

        # 2️⃣ Find missing parameters
        missing_names = parameter_names - set(existing_map.keys())

        new_parameters = []

        for name in missing_names:
            param = TelemetryParameter(
                satellite_id=satellite_id,
                name=name,
            )
            self.db.add(param)
            new_parameters.append(param)

        # 3️⃣ Flush once to get IDs
        self.db.flush()

        # 4️⃣ Build final map
        for param in new_parameters:
            existing_map[param.name] = param

        return existing_map