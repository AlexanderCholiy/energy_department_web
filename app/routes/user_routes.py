import os

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.check_authorization import check_authorization
from app.common.generate_pswd import get_password_hash, verify_password
from app.models.models_user import User
from database.db_users import get_db
from settings.urls import urls

CURRENT_DIR: str = os.path.dirname(__file__)
router = APIRouter()

directory: str = os.path.join(
    CURRENT_DIR, '..', '..', '..', 'templates', 'uptc'
)
templates = Jinja2Templates(directory=directory)


def set_error_message(request, message: str) -> RedirectResponse:
    request.session['message'] = message
    request.session['message_type'] = 'error'
    return RedirectResponse(
        url=request.headers.get('referer'),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post(urls.user)
async def update_profile(
    request: Request, db: Session = Depends(get_db),
    first_name: str = Form(...),
    last_name: str = Form(...),
    current_password: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
) -> Response:
    """Обновление данных пользователя."""

    user, redirect_response = await check_authorization(request, db)
    user_data = db.query(User).filter(User.useremail == user.useremail).first()

    if redirect_response:
        return redirect_response

    if not verify_password(current_password, user_data.hashed_password):
        return set_error_message(request, 'Проверьте текущий пароль.')

    if password != confirm_password:
        return set_error_message(request, 'Пароли не совпадают.')

    if password and len(password) < 10:
        return set_error_message(
            request, 'Пароль должен содержать минимум 10 символов.'
        )

    user_data.first_name = first_name
    user_data.last_name = last_name

    if password:
        user_data.hashed_password = get_password_hash(password)

    try:
        db.commit()
        db.refresh(user_data)
    except KeyboardInterrupt:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        return set_error_message(
            request, 'Ошибка при обновлении данных.'
        )

    request.session['message'] = 'Данные успешно обновлены!'
    request.session['message_type'] = 'success'

    return RedirectResponse(
        url=request.headers.get('referer'),
        status_code=status.HTTP_303_SEE_OTHER
    )
