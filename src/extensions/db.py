from sqlalchemy import create_engine
from sqlalchemy import sessionmaker

Data_base_url = "sqlite:///./sql_app.db"
engine = create_engine(Data_base_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
