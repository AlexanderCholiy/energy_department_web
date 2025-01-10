import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..'))
from app.models.models_user import Base, User  # noqa: E402

DATABASE_URL = f'sqlite:///{os.path.join(CURRENT_DIR, "uptc.db")}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    new_user = User(
        useremail="p.makurov@newtowers.ru",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$zrlXyjmndG5NidEaQ+id0w$2MNlsN86ZWna74I38/eeqViksbXVeFmo6rE0SKHTfgo"
    )
    db = next(get_db())
    db.add(new_user)
    db.commit()
