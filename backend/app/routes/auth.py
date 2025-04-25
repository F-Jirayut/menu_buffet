from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin, UserProfile
from app.controllers import user_controller
from app.utils.auth import create_access_token, verify_password
from app.database import Database
from app.schemas.base_response import BaseResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

db_instance = Database()
get_db = db_instance.get_db

@router.post("/login", response_model=BaseResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, user.username)
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "id": db_user.id, 
        "username": db_user.username, 
        "role_id": db_user.role.id, 
        "role_name": db_user.role.name,
        "permissions": [item.name for item in db_user.role.permissions]
    })
    return BaseResponse(
        success=True,
        message="Login successful",
        data={"access_token": access_token, "token_type": "bearer"}
    )

@router.get("/profile", response_model=BaseResponse[UserProfile])
def get_profile(payload = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_id(db, payload.get("id"))
    user_profile = UserProfile(
            id=db_user.id,
            name=db_user.name,
            username=db_user.username,
            role_id=db_user.role.id,
            role_name=db_user.role.name,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            permissions=[item.name for item in db_user.role.permissions]
        )
    return BaseResponse(
        success=True,
        message="User profile fetched successfully",
        data=user_profile
    )
