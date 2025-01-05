from fastapi import Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.common.authorization import get_current_user
from settings.urls import urls


async def check_authorization(request: Request, db: Session) -> tuple:
    """Проверяет авторизацию пользователя по токену."""
    token = request.cookies.get('access_token')

    if not token:
        return None, RedirectResponse(
            url=f'{urls.authorize}?error=ваша сессия истекла',
            status_code=status.HTTP_303_SEE_OTHER
        )

    user = await get_current_user(token, db)

    if user is None:
        return None, RedirectResponse(
            url=urls.authorize, status_code=status.HTTP_303_SEE_OTHER
        )

    return user, None
