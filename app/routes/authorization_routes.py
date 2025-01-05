import os
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.authorization import (authenticate_user, create_access_token,
                                      get_current_user)
from database.db_users import get_db
from settings.config import web_settings
from settings.urls import urls

CURRENT_DIR: str = os.path.dirname(__file__)
router = APIRouter()

directory: str = os.path.join(
    CURRENT_DIR, '..', '..', 'templates', 'authorization'
)
templates = Jinja2Templates(directory=directory)


@router.get(urls.index)
async def index(
    request: Request, token: str | None = None, db: Session = Depends(get_db)
) -> RedirectResponse:
    """
    Проверка токена аутентификации для доступа к главной странице приложения.
    Если токен действителен, пользователь существует и не заблокирован,
    отображается домашняя страница. В противном случае пользователь
    перенаправляется на страницу авторизации.
    """
    token = request.cookies.get('access_token')
    if token:
        user = await get_current_user(token, db)
        if user:
            return RedirectResponse(
                url=urls.home_uptc, status_code=status.HTTP_303_SEE_OTHER
            )
    return RedirectResponse(
        url=urls.authorize, status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(urls.authorize)
async def authorize(request: Request) -> HTMLResponse:
    """Страница авторизации пользователя."""
    error = request.query_params.get('error')
    context: dict = {
        'request': request,
        'error': error,
        'urls': urls,
    }
    return templates.TemplateResponse('authorization.html', context)


@router.post(urls.token)
async def login_for_access_token(
    request: Request,
    useremail: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """
    Если аутентификация успешна, создается токен доступа. Токен содержит данные
    о пользователе (в данном случае его электронную почту) и устанавливает
    время действия токена. Если пользователь не найден или не правильный логин
    и(или) пароль, пользователь заблокирован, тогда происходит перенаправление
    на страницу авторизации с сообщением об ошибке.
    """

    user = authenticate_user(db, useremail, password)
    if isinstance(user, int):
        error_messages = {
            1001: 'пользователь не найден',
            1002: 'неправильный логин или пароль',
            1003: 'вы заблокированы',
        }

        response = RedirectResponse(
            url=f'{urls.authorize}?error={error_messages[user]}',
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.delete_cookie('access_token')
        response.delete_cookie('saved_password')
        return response

    access_token_expires = timedelta(
        minutes=web_settings.WEB_SECURITY_ACCESS_TOKEN_EXPIRE_SECONDS
    )
    access_token = create_access_token(
        user_data=user,
        expires_delta=access_token_expires
    )

    response = RedirectResponse(
        url=urls.home_uptc, status_code=status.HTTP_303_SEE_OTHER
    )
    cookie_time = web_settings.WEB_SECURITY_ACCESS_TOKEN_EXPIRE_SECONDS
    response.set_cookie(
        key='access_token',
        value=f'Bearer {access_token}',
        httponly=True,
        max_age=cookie_time
    )

    if remember_me:
        response.set_cookie(
            key='saved_useremail', value=useremail, max_age=cookie_time
        )
        response.set_cookie(
            key='saved_password', value=password, max_age=cookie_time
        )
        response.set_cookie(
            key='remember_me', value='true', max_age=cookie_time
        )
    else:
        response.delete_cookie('saved_useremail')
        response.delete_cookie('saved_password')
        response.delete_cookie('remember_me')

    return response


@router.get(urls.logout)
@router.post(urls.logout)
async def logout(request: Request) -> RedirectResponse:
    """
    Выход пользователя из системы, удаление токена и перенаправление на
    страницу авторизации.
    """
    response = RedirectResponse(
        url=urls.authorize, status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie('access_token')
    return response
