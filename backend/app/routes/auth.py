from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin, User
from app.controllers import user_controller
from app.utils.auth import create_access_token, verify_password
from app.database import Database

router = APIRouter(prefix="/auth", tags=["Authentication"])

db_instance = Database()
get_db = db_instance.get_db

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, user.username)
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
