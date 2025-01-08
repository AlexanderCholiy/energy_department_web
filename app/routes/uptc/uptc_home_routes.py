import os

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, RedirectResponse
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
@router.get(urls.uptc_claims_all)
@router.get(urls.uptc_claims_mosoblenergo)
@router.get(urls.uptc_claims_portal)
@router.get(urls.uptc_claims_tatarstan)
@router.get(urls.uptc_claims_oboronenergo)
@router.get(urls.uptc_claims_rzd)
@router.get(urls.uptc_claims_rossetimr)
@router.get(urls.uptc_appeals_all)
@router.get(urls.uptc_appeals_portal)
@router.get(urls.uptc_appeals_oboronenergo)
@router.get(urls.uptc_appeals_rossetimr)
@router.post(urls.home_uptc)
@router.post(urls.uptc_claims_all)
@router.post(urls.uptc_claims_mosoblenergo)
@router.post(urls.uptc_claims_portal)
@router.post(urls.uptc_claims_tatarstan)
@router.post(urls.uptc_claims_oboronenergo)
@router.post(urls.uptc_claims_rzd)
@router.post(urls.uptc_claims_rossetimr)
@router.post(urls.uptc_appeals_all)
@router.post(urls.uptc_appeals_portal)
@router.post(urls.uptc_appeals_oboronenergo)
@router.post(urls.uptc_appeals_rossetimr)
async def handle_home_uptc(
    request: Request,
    db: Session = Depends(get_db),
    search_query: str = Form('')
) -> Response:
    """Поиск заявок и обращений."""

    user, redirect_response = await check_authorization(request, db)
    if redirect_response:
        return redirect_response

    current_path = request.url.path

    if request.method == 'POST' and not search_query:
        return RedirectResponse(
            url=current_path, status_code=status.HTTP_303_SEE_OTHER
        )

    if request.method == 'POST':
        content = (
            f'Контент из {__name__} (POST) для {current_path}'
            + (f' ({search_query})' if search_query else '')
        )
    else:
        content = (
            f'Контент из {__name__} (GET) для {current_path}'
            + (f' ({search_query})' if search_query else '')
        )        

    context = {
        'request': request,
        'urls': urls,
        'current_path': current_path,
        'user': user,
        'search_query': search_query,
        'content': content,
    }

    return templates.TemplateResponse('home_uptc.html', context)
