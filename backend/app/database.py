from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from app.config import settings
import time

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

MAX_RETRIES = 10
RETRY_DELAY = 3

for i in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        with engine.connect() as connection:
            print("Database is ready!")
        break
    except OperationalError as e:
        print(f"Database not ready yet (attempt {i+1}/{MAX_RETRIES}): {e}")
        time.sleep(RETRY_DELAY)
else:
    raise RuntimeError("Database not available after multiple retries")

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
