from app.models import StoreReservationOverride
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, time

def run():
    print("Seeding store reservation override...")

    db = SessionLocal()
    try:
        data = [
            {
                "date": date(2025, 5, 1),
                "open_time": None,
                "close_time": None,
                "is_closed": True,
                "note": "วันแรงงาน หยุดทำการ"
            },
            {
                "date": date(2025, 5, 2),
                "open_time": time(13, 0),
                "close_time": time(17, 0),
                "is_closed": False,
                "note": "เปิดเฉพาะช่วงบ่าย"
            }
        ]

        for item in data:
            existing = db.query(StoreReservationOverride).filter_by(date=item["date"]).first()
            if existing:
                print(f"Skipped: Already exists for date {item['date']}")
                continue

            override = StoreReservationOverride(**item)
            db.add(override)

        db.commit()
        print("Seeding store reservation override completed.")

    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
