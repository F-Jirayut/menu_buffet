from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import user_controller
from app.schemas.user import UserCreate, User
from app.database import Database

router = APIRouter(prefix="/users", tags=["Users"])

db_instance = Database()
get_db = db_instance.get_db

@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=User)
def user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user_by_id(db, id=user_id)
