import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    class Config:
        env_file = ".env"

settings = Settings()
