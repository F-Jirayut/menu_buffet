from app.models import StoreReservationSetting
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import time

def run():
    print("Seeding store reservation setting...")

    db = SessionLocal()
    try:
        data = [
            {"day_of_week": 0, "open_time": None, "close_time": None, "is_active": False},
            {"day_of_week": 1, "open_time": time(9, 0), "close_time": time(18, 0), "is_active": True},
            {"day_of_week": 2, "open_time": time(9, 0), "close_time": time(18, 0), "is_active": True},
            {"day_of_week": 3, "open_time": time(9, 0), "close_time": time(18, 0), "is_active": True},
            {"day_of_week": 4, "open_time": time(9, 0), "close_time": time(18, 0), "is_active": True},
            {"day_of_week": 5, "open_time": time(9, 0), "close_time": time(18, 0), "is_active": True},
            {"day_of_week": 6, "open_time": None, "close_time": None, "is_active": False},  # ปิดวันเสาร์
        ]

        for item in data:
            existing = db.query(StoreReservationSetting).filter_by(day_of_week=item["day_of_week"]).first()
            if existing:
                print(f"Skipped: Already exists for day_of_week {item['day_of_week']}")
                continue

            setting = StoreReservationSetting(**item)
            db.add(setting)

        db.commit()
        print("Seeding store reservation setting completed.")

    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
