import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status, Request
from app.models import Menu, MenuCategory
from app.schemas.menu import MenuCreate, MenuUpdate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config import settings
from slugify import slugify
from sqlalchemy import func
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.utils.s3 import upload_file_s3, delete_file_s3  

def create_menu(
    db: Session,
    menu: MenuCreate,
    image: UploadFile = None
):
    existing_menu = db.query(Menu).filter(Menu.name == menu.name).first()
    if existing_menu:
        raise HTTPException(status_code=400, detail=f"Menu with name '{menu.name}' already exists.")

    category = db.query(MenuCategory).filter(MenuCategory.id == menu.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail=f"Menu category ID {menu.category_id} does not exist.")

    try:
        image_disk = None
        image_path = None

        if image:
            now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            original_filename = os.path.splitext(image.filename)[0]
            extension = os.path.splitext(image.filename)[1]
            safe_name = slugify(original_filename)
            filename = f"{now_str}-{safe_name}{extension}"
            image_disk = settings.STORAGE_DISK

            if image_disk == "local":
                path = f"uploads/menus/{filename}"
                full_path = os.path.join("storage", path)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, "wb") as f:
                    f.write(image.file.read())

                image_path = path
            elif image_disk == "s3":
                path = f"uploads/menus/{filename}"
                try:
                    upload_file_s3(image, path)
                    image_path = path
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))

        sort_order = menu.sort_order
        if sort_order is None:
            max_sort = db.query(func.max(Menu.sort_order)).scalar() or 0
            sort_order = max_sort + 1

        db_menu = Menu(
            name=menu.name,
            description=menu.description or None,
            category_id=menu.category_id,
            is_available=menu.is_available,
            image_disk=image_disk,
            image_path=image_path,
            sort_order=sort_order
        )

        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error creating menu ")

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

def get_menus(db: Session):
    return db.query(Menu).order_by(Menu.sort_order).all()
    
def get_menu_by_id(db: Session, id: int, request: Request = None):
    return db.query(Menu).filter(Menu.id == id).first()

def update_menu(db: Session, menu_id: int, menu, image: UploadFile = None):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    existing = db.query(Menu).filter(Menu.name == menu.name, Menu.id != menu_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Menu with name '{menu.name}' already exists.")

    try:
        db_menu.name = menu.name
        db_menu.description = menu.description or None
        db_menu.category_id = menu.category_id
        db_menu.is_available = menu.is_available
        db_menu.sort_order = menu.sort_order

        if image:
            if db_menu.image_path:
                try:
                    if db_menu.image_disk == "local":
                        old_path = os.path.join("storage", db_menu.image_path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    elif db_menu.image_disk == "s3":
                        delete_file_s3(db_menu.image_path)
                except Exception as e:
                    print(f"Warning: Failed to delete old image: {str(e)}")

            now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            original_filename = os.path.splitext(image.filename)[0]
            extension = os.path.splitext(image.filename)[1]
            safe_name = slugify(original_filename)
            filename = f"{now_str}-{safe_name}{extension}"
            image_disk = settings.STORAGE_DISK
            path = f"uploads/menus/{filename}"

            if image_disk == "local":
                full_path = os.path.join("storage", path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "wb") as f:
                    f.write(image.file.read())
            elif image_disk == "s3":
                upload_file_s3(image, path)
            else:
                raise HTTPException(status_code=500, detail="Invalid image disk setting")

            db_menu.image_path = path
            db_menu.image_disk = image_disk

        db.commit()
        db.refresh(db_menu)
        return db_menu

    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error updating menu")

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    image_disk = db_menu.image_disk
    image_path = db_menu.image_path

    try:
        db.delete(db_menu)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting menu")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    if image_path:
        try:
            if image_disk == "local":
                file_path = os.path.join("storage", image_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
            elif image_disk == "s3":
                delete_file_s3(image_path)
        except Exception as e:
            print(f"Warning: Failed to delete image: {str(e)}")

    return {"message": "Menu deleted successfully"}


