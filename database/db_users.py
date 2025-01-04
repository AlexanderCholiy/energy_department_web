import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..', '..'))
from settings.config import db_settings  # noqa: E402


SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{db_settings.DB_USER}:{db_settings.DB_PSWD}' +
    f'@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME_WEB}'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
