from sqlalchemy import func

from app.ai.tools.base import Tool
from app.core.database import SessionLocal
from app.satellites.domain.models import Satellite


class SatelliteCountTool(Tool):

    name = "satellite_count"

    def execute(self):

        db = SessionLocal()

        count = db.query(func.count(Satellite.id)).scalar()

        db.close()

        return f"There are {count} satellites registered."


class SatelliteListTool(Tool):

    name = "satellite_list"

    def execute(self):

        db = SessionLocal()

        satellites = db.query(Satellite).all()

        db.close()

        if not satellites:
            return "No satellites registered."

        return "\n".join(
            satellite.name
            for satellite in satellites
        )