from app.models import MenuCategory
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

def run():
    print("Seeding menu_categories...")

    db = SessionLocal()
    try:
        menu_categories = [
            {"name": "เนื้อหมู", "description": "เนื้อหมูสดสำหรับทำอาหาร"},
            {"name": "เนื้อไก่", "description": "เนื้อไก่สดสำหรับทำอาหาร"},
            {"name": "เนื้อวัว", "description": "เนื้อวัวสดสำหรับทำอาหาร"},
            {"name": "อาหารทะเล", "description": "อาหารทะเลสดสำหรับทำอาหาร"},
            {"name": "ผักสด", "description": "ผักสดสำหรับทำอาหาร"},
            {"name": "ข้าว", "description": "ข้าวสวย ข้าวผัด ข้าวต้ม"},
            {"name": "เส้น", "description": "เส้นก๋วยเตี๋ยว เส้นหมี่ เส้นสปาเก็ตตี้"},
            {"name": "ของทอด", "description": "อาหารประเภททอด เช่น นักเก็ต ไก่ทอด"},
            {"name": "ซูชิ", "description": "ข้าวปั้นหน้าต่างๆ"},
            {"name": "สลัด", "description": "ผักสด น้ำสลัด และเครื่องเคียง"},
            {"name": "ของหวาน", "description": "ไอศกรีม ขนมหวาน และผลไม้"},
            {"name": "เครื่องดื่ม", "description": "น้ำอัดลม น้ำผลไม้ น้ำเปล่า"},
        ]

        for cat in menu_categories:
            if not db.query(MenuCategory).filter_by(name=cat["name"]).first():
                max_sort = db.query(func.max(MenuCategory.sort_order)).scalar() or 0
                new_sort_order = max_sort + 1

                menucategory = MenuCategory(
                    name=cat["name"],
                    description=cat["description"],
                    sort_order=new_sort_order
                )
                db.add(menucategory)
                db.commit()
                print(f"MenuCategory '{cat['name']}' seeded with sort_order {new_sort_order}.")
            else:
                print(f"MenuCategory '{cat['name']}' already exists.")

    except SQLAlchemyError as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()
