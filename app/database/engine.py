import os
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

database_engine = os.getenv("DATABASE_ENGINE")
pool_size_str = os.getenv("DATABASE_POOL_SIZE", "10")
pool_size = int(pool_size_str)

engine = create_engine(database_engine, pool_size=pool_size)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False