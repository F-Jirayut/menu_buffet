from sqlalchemy.orm import Session
from app.models import MenuCategory
from app.schemas.menu_category import MenuCategoryCreate, MenuCategoryUpdate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.auth import hash_password
from fastapi import HTTPException, status
from sqlalchemy import func

def create_menu_category(db: Session, menu_category: MenuCategoryCreate):
    try:
        existing_menu_category = db.query(MenuCategory).filter(MenuCategory.name == menu_category.name).first()
        if existing_menu_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu category already exists."
            )
        
        sort_order = menu_category.sort_order
        if menu_category.sort_order is None:
            max_sort = db.query(func.max(MenuCategory.sort_order)).scalar() or 0
            sort_order = max_sort + 1

        db_menu_category = MenuCategory(
            name=menu_category.name,
            description=menu_category.description,
            sort_order=sort_order
        )

        db.add(db_menu_category)
        db.commit()
        db.refresh(db_menu_category)

        return db_menu_category

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    
def get_menu_category_by_id(db: Session, id: int):
    db_menu_category = db.query(MenuCategory).filter(MenuCategory.id == id).first()
    if db_menu_category is None:
        raise HTTPException(status_code=404, detail="Menu category not found")
    return db_menu_category

def get_menu_categories(db: Session):
    return db.query(MenuCategory).order_by(MenuCategory.sort_order).all()

def update_menu_category(db: Session, menu_category_id: int, menu_category: MenuCategoryUpdate):
    db_menu_category = db.query(MenuCategory).filter(MenuCategory.id == menu_category_id).first()
    if not db_menu_category:
        raise HTTPException(status_code=404, detail="Menu category not found")

    duplicate = db.query(MenuCategory).filter(
        MenuCategory.name == menu_category.name,
        MenuCategory.id != menu_category_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Menu category name already exists")

    db_menu_category.name = menu_category.name
    db_menu_category.description = menu_category.description
    db_menu_category.sort_order = menu_category.sort_order

    try:
        db.commit()
        db.refresh(db_menu_category)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating menu category")

    return db_menu_category


def delete_menu_category(db: Session, menu_category_id: int):
    db_menu_category = db.query(MenuCategory).filter(MenuCategory.id == menu_category_id).first()
    if not db_menu_category:
        raise HTTPException(status_code=404, detail="Menu category not found")
    try:
        db.delete(db_menu_category)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting menu category")
    
    return {"message": "Menu category deleted successfully"}