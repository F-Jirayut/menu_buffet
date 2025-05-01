from app.models import Table
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def run():
    print("Seeding tables...")

    db = SessionLocal()
    try:
        existing_names = {t.name for t in db.query(Table.name).all()}

        base_tables = [
            ("Table A", 4),
            ("Table B", 4),
            ("Table C", 6),
            ("Table D", 4),
            ("Table E", 8),
            ("Table F", 6),
            ("Table G", 8),
            ("Table H", 4),
            ("Table I", 8),
            ("Table J", 4),
            ("Table K", 8),
            ("Table L", 4),
            ("Table O", 8),
            ("Table M", 4),
            ("Table N", 8),
        ]

        tables_to_insert = []
        for idx, (name, capacity) in enumerate(base_tables, start=1):
            if name not in existing_names:
                tables_to_insert.append(
                    Table(
                        name=name,
                        capacity=capacity,
                        note="General",
                        is_active=True,
                        sort_order=idx
                    )
                )

        if tables_to_insert:
            db.add_all(tables_to_insert)
            db.commit()
            print(f"Seeded {len(tables_to_insert)} new tables.")
        else:
            print("All tables already exist. Nothing to seed.")

    except SQLAlchemyError as e:
        print(f"Error during table seeding: {e}")
        db.rollback()
    finally:
        db.close()
