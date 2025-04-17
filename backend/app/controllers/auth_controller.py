from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import verify_password, create_access_token
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserLogin

def login(db: Session, form_data: UserLogin):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
