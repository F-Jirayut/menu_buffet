from sqlalchemy import Column, BigInteger, String, Text, Boolean, ForeignKey, TIMESTAMP, func, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from app.config import settings 
from app.utils.s3 import generate_presigned_url

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_disk = Column(String(50), nullable=True)
    image_path = Column(Text, nullable=True)
    category_id = Column(BigInteger, ForeignKey('menu_categories.id'), nullable=False)
    is_available = Column(Boolean, nullable=False, server_default='true')
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    menu_category = relationship("MenuCategory", back_populates="menus")

    @property
    def image_url(self):
        if not self.image_path:
            return None

        if self.image_disk == "local":
            return f"{settings.APP_URL}/storage/{self.image_path}"
        elif self.image_disk == "s3":
            return generate_presigned_url(self.image_path)
        else:
            return None
