import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_URL = os.getenv("APP_URL", "http://localhost:8000")
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    WEB_FRONT_URL = os.getenv("WEB_FRONTEND_URL", "http://localhost:5173")

    STORAGE_DISK = os.getenv("STORAGE_DISK", "local")
    
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_REGION = os.getenv("AWS_REGION")
    
    class Config:
        env_file = ".env"

settings = Settings()
