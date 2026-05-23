from uuid import UUID

from app.core.database import SessionLocal
from app.satellites.domain.models import Satellite

SATELLITES = [
    {
        "id": UUID("af6f1df7-da0d-437f-9b01-4836cec81212"),
        "name": "ISS",
        "norad_id": 25544,
        "orbit_type": "LEO",
    },
    {
        "id": UUID("2c50054c-604c-460b-bd52-bedc9941ae78"),
        "name": "GPS IIR-10",
        "norad_id": 20580,
        "orbit_type": "MEO",
    },
    {
        "id": UUID("3f174425-3b65-4ae1-a7f9-1f73c8c077a6"),
        "name": "Terra",
        "norad_id": 39634,
        "orbit_type": "LEO",
    },
]

def seed():
    db = SessionLocal()

    existing = db.query(Satellite).count()
    if existing > 0:
        print("Already seeded")
        return

    for s in SATELLITES:
        db.add(Satellite(**s))

    db.commit()
    db.close()

    print("Seed completed")

if __name__ == "__main__":
    seed()