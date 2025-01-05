import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.check_authorization import check_authorization
from database.db_users import get_db
from settings.urls import urls

CURRENT_DIR: str = os.path.dirname(__file__)
router = APIRouter()

directory: str = os.path.join(
    CURRENT_DIR, '..', '..', '..', 'templates', 'uptc'
)
templates = Jinja2Templates(directory=directory)


@router.get(urls.home_uptc)
async def home_uptc(
    request: Request, db: Session = Depends(get_db)
) -> Response:
    """Домашняя страница со всеми последними заявками и обращениями."""

    user, redirect_response = await check_authorization(request, db)

    if redirect_response:
        return redirect_response

    context: dict = {
        'request': request,
        'urls': urls,
        'user': user,
    }
    return templates.TemplateResponse('home_uptc.html', context)
