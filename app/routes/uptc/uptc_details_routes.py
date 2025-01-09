import os

from fastapi import APIRouter, Depends, Request, Form, status, Path
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import conint

from app.common.check_authorization import check_authorization
from database.db_users import get_db
from database.db_base import sql_queries
from database.requests.select_claims import select_claims
from settings.urls import urls

CURRENT_DIR: str = os.path.dirname(__file__)
router = APIRouter()

directory: str = os.path.join(
    CURRENT_DIR, '..', '..', '..', 'templates', 'uptc'
)
templates = Jinja2Templates(directory=directory)

PERSONAL_AREA: dict[str, list[int]] = {
    urls.uptc_claims_portal: [1],
    urls.uptc_appeals_portal: [1],
    urls.uptc_claims_mosoblenergo: [2],
    urls.uptc_claims_tatarstan: [3],
    urls.uptc_claims_rzd: [4],
    urls.uptc_claims_oboronenergo: [5],
    urls.uptc_appeals_oboronenergo: [5],
    urls.uptc_claims_rossetimr: [6],
    urls.uptc_appeals_rossetimr: [6],
}

NULL_VALUE: str = 'NaN'


@router.get(urls.uptc_claims_all + '/{number}')
@router.get(urls.uptc_appeals_all + '/{number}')
async def handle_home_uptc(
    request: Request,
    number: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    search_query: str = Form('')
) -> Response:
    """Подробная информация по заявкам и обращениям."""

    user, redirect_response = await check_authorization(request, db)
    if redirect_response:
        return redirect_response

    current_path = request.url.path

    table = sql_queries(
        select_claims(
            claim_id=search_query,
            null_value=NULL_VALUE
        ),
        'tech_pris'
    )

    context = {
        'request': request,
        'urls': urls,
        'current_path': current_path,
        'user': user,
        'search_query': search_query,
        'table': table,
        'null_value': NULL_VALUE,
    }

    return templates.TemplateResponse('claims.html', context)
