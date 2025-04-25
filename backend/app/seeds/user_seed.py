from app.models import User, Role
from app.utils.auth import hash_password
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def run():
    print("Seeding users...")

    db = SessionLocal()
    try:
        root_role = db.query(Role).filter_by(name="root").first()
        if not root_role:
            print("Root role not found. Skipping user seed.")
            return

        if not db.query(User).filter_by(username="root").first():
            user = User(
                name="Root",
                username="root",
                password=hash_password("password"),
                role_id=root_role.id
            )
            db.add(user)
            db.commit()
            print("Root user seeded.")
        else:
            print("Root user already exists.")

        admin_role = db.query(Role).filter_by(name="admin").first()
        if not admin_role:
            print("No admin role found. Skipping user seed.")
            return

        if not db.query(User).filter_by(username="admin").first():
            user = User(
                name="Admin",
                username="admin",
                password=hash_password("password"),
                role_id=admin_role.id
            )
            db.add(user)
            db.commit()
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")
    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
