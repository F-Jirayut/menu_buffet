from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Database:
    def __init__(self):
        self.session_local = SessionLocal

    def get_db(self):
        print(">>> create DB session")
        db: Session = self.session_local()
        try:
            yield db
        finally:
            print(">>> close DB session")
            db.close()
