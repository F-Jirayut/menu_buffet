from app.models import Role, Permission
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def run():
    print("Seeding root role with all permissions...")

    db = SessionLocal()
    try:
        # Find or create Root role
        role = db.query(Role).filter_by(name="root").first()
        if not role:
            role = Role(name="root")
            db.add(role)
            db.commit()
            db.refresh(role)
            print("Created 'root' role.")
        else:
            print("'root' role already exists.")

        # Get all permissions
        all_permissions = db.query(Permission).all()

        # Assign all permissions to Root role
        existing_permission_ids = {p.id for p in role.permissions}
        new_permissions = [p for p in all_permissions if p.id not in existing_permission_ids]

        if new_permissions:
            role.permissions.extend(new_permissions)
            db.commit()
            print(f"Added {len(new_permissions)} new permissions to 'Root' role.")
        else:
            print("Root role already has all permissions.")

    except SQLAlchemyError as e:
        print(f"Error during role-permission seeding: {e}")
        db.rollback()
    finally:
        db.close()
