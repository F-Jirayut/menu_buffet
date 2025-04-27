from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.controllers import menu_controller
from app.schemas.menu import MenuResponse, MenuCreate, MenuUpdate
from app.models import Menu
from app.schemas.base_response import BaseResponse
from app.schemas.pagination import Pagination
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items
import qrcode
import io

db_instance = Database()
get_db = db_instance.get_db
prefix = "/buffet_sessions"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["BuffetSession.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["BuffetSession.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["BuffetSession.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["BuffetSession.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["BuffetSession.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["BuffetSessions"],
    dependencies=[
        Depends(get_current_user),
        # Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.get("/generate_qr")
async def generate_qr(text: str = Query(..., description="Text to encode into QR Code")):
    # สร้าง QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # เซฟลง memory buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # ส่งกลับเป็นรูปภาพ
    return StreamingResponse(buf, media_type="image/png")


