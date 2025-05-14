from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import os
from app.routes import user, role, auth, permission, menu_category, menu, option, table, order, customer
from app.database import Base, engine
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.WEB_FRONT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ใช้ __file__ เพื่อให้แน่ใจว่า path ถูกต้องทั้งใน local และ Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
menus_dir = os.path.join(BASE_DIR, "..", "storage", "uploads", "menus")

# ✅ ตรวจสอบว่า directory มีอยู่จริง ถ้าไม่มีให้สร้างเลย
if not os.path.exists(menus_dir):
    os.makedirs(menus_dir)

app.mount("/storage/uploads/menus", StaticFiles(directory=menus_dir), name="menus")

Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user.router, prefix="/api")
app.include_router(role.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(permission.router, prefix="/api")
app.include_router(menu_category.router, prefix="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(option.router, prefix="/api")
app.include_router(table.router, prefix="/api")
app.include_router(order.router, prefix="/api")
app.include_router(customer.router, prefix="/api")
