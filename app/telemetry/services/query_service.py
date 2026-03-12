from app.telemetry.infrastructure.repository import TelemetryRepository


MAX_LIMIT = 1000


class TelemetryQueryService:

    def __init__(self, db):
        self.repo = TelemetryRepository(db)

    def get_telemetry(
        self,
        satellite_id,
        start_time=None,
        end_time=None,
        cursor=None,
        limit=100,
    ):

        if limit > MAX_LIMIT:
            limit = MAX_LIMIT

        return self.repo.get_window(
            satellite_id=satellite_id,
            start_time=start_time,
            end_time=end_time,
            cursor=cursor,
            limit=limit,
        )