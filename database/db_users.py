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
    from app.common.generate_pswd import get_password_hash

    useremail: str = input('Введите email пользователя: ').strip()
    password: str = input('Введите пароль пользователя: ').strip()
    if not password or not useremail:
        raise ValueError('Email или пароль не могут быть пустыми.')
    write_flag: bool = input(
        f'Пользователь: {useremail}\nПароль: {password}\nПродолжить? (Y/N): '
    ).lower() == 'y'

    if not write_flag:
        sys.exit(0)

    Base.metadata.create_all(engine)
    new_user = User(
        useremail=useremail,
        hashed_password=get_password_hash(password)
    )
    db = next(get_db())
    db.add(new_user)
    db.commit()
