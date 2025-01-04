import os
import sys

from fastapi import Depends
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from pydantic import EmailStr
from sqlalchemy.orm import Session

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, '..', '..')))
from settings.config import web_settings  # noqa: E402
from app.common.generate_pswd import (  # noqa: E402
    verify_password, oauth2_scheme
)
from app.models.models_user import UserInDB, User  # noqa: E402
from database.db_users import get_db  # noqa: E402


def authenticate_user(
    db: Session, useremail: EmailStr, password: str
) -> UserInDB | int:
    """
    Авторизация пользоваетля.
    - Если пользователя нет в БД -> 1001;
    - Если не правильный логин/пароль -> 1002;
    - Если пользователь был заблокирован -> 1003;
    """
    user_data = db.query(User).filter(User.useremail == useremail).first()
    if not user_data:
        return 1001
    if not user_data.is_active:
        return 1003
    if not verify_password(password, user_data.hashed_password):
        return 1002

    return UserInDB(user_data)


def create_access_token(
    user_data: UserInDB, expires_delta: Optional[timedelta] = None
) -> str:
    """Создаем JWT токен для пользователя."""
    to_encode = user_data.__dict__.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})  # Добавляем время истечения токена.
    encoded_jwt = jwt.encode(
        to_encode,
        web_settings.WEB_SECURITY_SECRET_KEY,
        algorithm=web_settings.WEB_SECURITY_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Функция предназначена для извлечения информации о текущем пользователе из
    предоставленного токена.
    """
    try:
        # Если токен содержит "Bearer " что характерно для алгоритма argon2,
        # удаляем его:
        token = token.split(" ")[1] if " " in token else token
        payload = jwt.decode(
            token,
            web_settings.WEB_SECURITY_SECRET_KEY,
            algorithms=[web_settings.WEB_SECURITY_ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")

        if email is None:
            return None

        user = db.query(User).filter(User.useremail == email).first()

        if not user:
            return None

        return user

    except JWTError:
        return None


if __name__ == '__main__':
    print(authenticate_user('user2@example.com', 'qwerty2'))
