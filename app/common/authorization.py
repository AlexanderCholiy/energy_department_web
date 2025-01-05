from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.common.generate_pswd import oauth2_scheme, verify_password
from app.models.models_user import User, UserBase
from database.db_users import get_db
from settings.config import web_settings


def authenticate_user(
    db: Session, useremail: EmailStr, password: str
) -> dict | int:
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

    return {'sub': useremail}


def create_access_token(
    user_data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Создаем JWT токен для пользователя."""
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({'exp': expire})  # Добавляем время истечения токена.

    encoded_jwt = jwt.encode(
        to_encode,
        web_settings.WEB_SECURITY_SECRET_KEY,
        algorithm=web_settings.WEB_SECURITY_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[UserBase]:
    """
    Функция предназначена для извлечения информации о текущем пользователе из
    предоставленного токена.
    """
    try:
        # Если токен содержит "Bearer " что характерно для алгоритма argon2,
        # удаляем его:
        token = token.split(' ')[1] if ' ' in token else token
        payload = jwt.decode(
            token,
            web_settings.WEB_SECURITY_SECRET_KEY,
            algorithms=[web_settings.WEB_SECURITY_ALGORITHM]
        )
        useremail: Optional[str] = payload.get('sub')

        if useremail is None:
            return None

        user_data = db.query(User).filter(User.useremail == useremail).first()

        if not user_data or not user_data.is_active:
            return None

        return UserBase(
            **{
                column.name: getattr(
                    user_data, column.name
                ) for column in User.__table__.columns
            }
        )

    except JWTError:
        return None

    except Exception as e:
        print(f'Ошибка в {__name__}:\n{str(e)}')
        return None
