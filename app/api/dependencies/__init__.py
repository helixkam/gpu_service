
from .db import SessionLocal, engine
from .base import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    Base.metadata.create_all(bind=engine)

