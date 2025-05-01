from app.models import Permission
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def run():
    print("Seeding permissions...")

    db = SessionLocal()
    try:
        permissions = [
            {"name": "Role.View", "description": "Can View Roles"},
            {"name": "Role.Create", "description": "Can Create Roles"},
            {"name": "Role.Update", "description": "Can Update Roles"},
            {"name": "Role.Delete", "description": "Can Delete Roles"},
            
            {"name": "User.View", "description": "Can View Users"},
            {"name": "User.Create", "description": "Can Create Users"},
            {"name": "User.Update", "description": "Can Update Users"},
            {"name": "User.Delete", "description": "Can Delete Users"},
            
            {"name": "Permission.View", "description": "Can View Permissions"},
            {"name": "Permission.Create", "description": "Can Create Permissions"},
            {"name": "Permission.Update", "description": "Can Update Permissions"},
            {"name": "Permission.Delete", "description": "Can Delete Permissions"},

            {"name": "Menu.View", "description": "Can View Menus"},
            {"name": "Menu.Create", "description": "Can Create Menus"},
            {"name": "Menu.Update", "description": "Can Update Menus"},
            {"name": "Menu.Delete", "description": "Can Delete Menus"},
            
            {"name": "Category.View", "description": "Can View Categories"},
            {"name": "Category.Create", "description": "Can Create Categories"},
            {"name": "Category.Update", "description": "Can Update Categories"},
            {"name": "Category.Delete", "description": "Can Delete Categories"}, 
            
            {"name": "Table.View", "description": "Can View Tables"},
            {"name": "Table.Create", "description": "Can Create Tables"},
            {"name": "Table.Update", "description": "Can Update Tables"},
            {"name": "Table.Delete", "description": "Can Delete Tables"}, 
            
            {"name": "Order.View", "description": "Can View Orders"},
            {"name": "Order.Create", "description": "Can Create Orders"},
            {"name": "Order.Update", "description": "Can Update Orders"},
            {"name": "Order.Delete", "description": "Can Delete Orders"}, 
        ]

        for perm in permissions:
            if not db.query(Permission).filter_by(name=perm["name"]).first():
                permission = Permission(name=perm["name"], description=perm["description"])
                db.add(permission)
                db.commit()
                print(f"Permission '{perm['name']}' seeded.")
            else:
                print(f"Permission '{perm['name']}' already exists.")

    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
