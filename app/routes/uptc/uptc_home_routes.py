import os

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.check_authorization import check_authorization
from database.db_users import get_db
from database.db_base import sql_queries
from database.requests.select_claims import select_claims
from database.requests.select_appeals import select_appeals
from database.requests.select_claims_and_appeals import (
    select_claims_and_appeals
)
from settings.urls import urls

router = APIRouter()
templates = Jinja2Templates(
    directory=os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'templates', 'uptc'
    )
)

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
    search_query = search_query.strip()

    if request.method == 'POST' and not search_query:
        return RedirectResponse(
            url=current_path, status_code=status.HTTP_303_SEE_OTHER
        )

    personal_area_id = PERSONAL_AREA.get(current_path, [1, 2, 3, 4, 5, 6])
    table, template_name, current_path = await fetch_data(
        current_path, search_query, personal_area_id
    )

    search_url = current_path if (
        current_path in PERSONAL_AREA.keys()
    ) else urls.home_uptc

    context = {
        'request': request,
        'urls': urls,
        'current_path': current_path,
        'user': user,
        'search_query': search_query,
        'search_url': search_url,
        'table': table,
        'null_value': NULL_VALUE,
    }

    return templates.TemplateResponse(template_name, context)


async def fetch_data(
    current_path: str, search_query: str, personal_area_id: list[int]
):
    if current_path == urls.home_uptc:
        return sql_queries(
            select_claims_and_appeals(
                search_query=search_query, null_value=NULL_VALUE
            ), 'tech_pris'
        ), 'home.html', current_path

    if current_path.startswith(urls.uptc_appeals_all):
        table = sql_queries(
            select_appeals(
                search_query=search_query,
                personal_area_id=personal_area_id,
                null_value=NULL_VALUE
            ), 'tech_pris'
        )
        if not table:
            table = sql_queries(
                select_appeals(
                    search_query=search_query, null_value=NULL_VALUE
                ), 'tech_pris'
            )
            current_path = urls.uptc_appeals_all
        return table, 'appeals.html', current_path

    table = sql_queries(
        select_claims(
            search_query=search_query,
            personal_area_id=personal_area_id,
            null_value=NULL_VALUE
        ), 'tech_pris'
    )
    if not table:
        table = sql_queries(
            select_claims(
                search_query=search_query, null_value=NULL_VALUE
            ), 'tech_pris'
        )
        current_path = urls.uptc_claims_all
    return table, 'claims.html', current_path
