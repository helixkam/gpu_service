from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

try:
    conn = engine.connect()
    print("Connect!")
    conn.close()
except Exception as e:
    print("Error: ", e)