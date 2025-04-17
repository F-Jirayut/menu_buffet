from fastapi import FastAPI
from app.routes import user, role, auth
from app.database import Base, engine
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user.router)
app.include_router(role.router)
app.include_router(auth.router)
# app.include_router(menu.router)
# app.include_router(buffet_session.router)
# app.include_router(order.router)
# app.include_router(menu_category.router)