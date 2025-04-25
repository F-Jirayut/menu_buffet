from sqlalchemy.orm import Session
from app.models import User, Role
from app.schemas.user import UserCreate
from sqlalchemy.exc import SQLAlchemyError
from app.utils.auth import hash_password
from fastapi import HTTPException, status

def get_user_by_id(db: Session, id: int):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken."
        )
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with ID {user.role_id} does not exist."
        )
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )

    db_user = User(
        name=user.name,
        username=user.username,
        password=hash_password(user.password),
        role_id=user.role_id,
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Could not create user."
        )
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with ID {user.role_id} does not exist."
        )

    if user.password:
        if len(user.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long."
            )
        db_user.password = hash_password(user.password)

    try:
        db_user.name = user.name
        db_user.username = user.username
        db_user.role_id = user.role_id
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error. Could not update user.")
    
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db.delete(db_user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error. Could not delete user.")
    
    return {"message": "User deleted successfully"}