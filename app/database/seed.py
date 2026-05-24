from app.core.database import SessionLocal
from app.satellites.domain.models import Satellite


SATELLITES = [
    {
        "name": "ISS",
        "norad_id": 25544,
        "orbit_type": "LEO",
    },
    {
        "name": "Hubble Space Telescope",
        "norad_id": 20580,
        "orbit_type": "LEO",
    },
    {
        "name": "Sentinel-1A",
        "norad_id": 39634,
        "orbit_type": "LEO",
    },
]


def seed():
    db = SessionLocal()

    try:

        for satellite_data in SATELLITES:

            existing = (
                db.query(Satellite)
                .filter(
                    Satellite.norad_id == satellite_data["norad_id"]
                )
                .first()
            )

            if not existing:

                satellite = Satellite(**satellite_data)

                db.add(satellite)

        db.commit()

        print("Seed completed")

    finally:
        db.close()


if __name__ == "__main__":
    seed()