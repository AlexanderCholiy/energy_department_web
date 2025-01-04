import os
import sys

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(
    os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', '..'))
)
from app.common.authorization import get_current_user  # noqa: E402
from database.db_users import get_db  # noqa: E402
from settings.urls import urls  # noqa: E402


router = APIRouter()

directory: str = os.path.join(
    CURRENT_DIR, '..', '..', '..', 'templates', 'uptc'
)
templates = Jinja2Templates(directory=directory)


@router.get(urls.home_uptc, response_class=RedirectResponse)
async def home_uptc(
    request: Request, token: str | None = None, db: Session = Depends(get_db)
) -> RedirectResponse:
    """Домашняя страница со всеми последними заявками и обращениями."""
    # token = request.cookies.get('access_token')
    # if token:
    #     user = await get_current_user(token, db)
    #     if user and user.is_active:
    #         return RedirectResponse(
    #             url=urls.home_uptc, status_code=status.HTTP_303_SEE_OTHER
    #         )
    context: dict = {
        'request': request,
        'urls': urls,
    }
    return templates.TemplateResponse('home_uptc.html', context)
