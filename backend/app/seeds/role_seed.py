from app.models import Role
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def run():
    print("Seeding roles...")

    db = SessionLocal()
    try:
        if not db.query(Role).filter_by(name="root").first():
            admin_role = Role(name="root")
            db.add(admin_role)
            db.commit()
            print("Root role seeded.")
        else:
            print("Root role already exists.")

        if not db.query(Role).filter_by(name="admin").first():
            user_role = Role(name="admin")
            db.add(user_role)
            db.commit()
            print("Admin role seeded.")
        else:
            print("Admin role already exists.")

    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
