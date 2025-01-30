import os
from typing import Optional

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from database.db_base import sql_queries
from database.requests.select_avr import select_avr
from settings.urls import urls

router = APIRouter()
templates = Jinja2Templates(
    directory=os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'templates', 'avr'
    )
)

RELEVANT_STATUS: dict[str, Optional[bool]] = {
    urls.home_avr: None,
    urls.avr_claims_all: None,
    urls.avr_claims_actual: True,
    urls.avr_claims_not_actual: False,
    urls.avr_dgu_actual: True,
    urls.avr_dgu_not_actual: False
}

NULL_VALUE: str = 'NaN'


@router.get(urls.home_avr)
@router.get(urls.avr_claims_all)
@router.get(urls.avr_claims_actual)
@router.get(urls.avr_claims_not_actual)
@router.get(urls.avr_dgu_actual)
@router.get(urls.avr_dgu_not_actual)
@router.post(urls.avr_claims_all)
@router.post(urls.avr_claims_actual)
@router.post(urls.avr_claims_not_actual)
@router.post(urls.avr_dgu_actual)
@router.post(urls.avr_dgu_not_actual)
async def handle_home_avr(
    request: Request, search_query: str = Form('')
) -> Response:
    """Поиск АВР"""
    current_path = request.url.path
    search_query = search_query.strip()

    if current_path == urls.home_avr:
        return RedirectResponse(
            url=urls.avr_claims_all, status_code=status.HTTP_303_SEE_OTHER
        )

    if request.method == 'POST' and not search_query:
        return RedirectResponse(
            url=current_path, status_code=status.HTTP_303_SEE_OTHER
        )

    table, template_name, current_path = await fetch_data(
        current_path, search_query
    )

    context = {
        'request': request,
        'urls': urls,
        'current_path': current_path,
        'search_query': search_query,
        'search_url': current_path,
        'table': table,
        'null_value': NULL_VALUE,
    }

    return templates.TemplateResponse(template_name, context)


async def fetch_data(current_path: str, search_query: str):
    is_status_relevant = RELEVANT_STATUS.get(current_path)
    if current_path in (
        urls.avr_claims_all, urls.avr_claims_actual, urls.avr_claims_not_actual
    ):
        table = sql_queries(
            select_avr(
                null_value=NULL_VALUE,
                number=search_query,
                is_status_relevant=is_status_relevant
            ), 'avr'
        )
        if not table:
            table = sql_queries(
                select_avr(
                    null_value=NULL_VALUE,
                    number=search_query,
                    is_status_relevant=None
                ), 'avr'
            )
            current_path = urls.avr_claims_all
        return table, 'claims.html', current_path

    table = sql_queries(
        select_avr(
            null_value=NULL_VALUE,
            number=search_query,
            is_status_relevant=is_status_relevant,
            filter_power_supply=True
        ), 'avr'
    )
    if not table:
        table = sql_queries(
            select_avr(
                null_value=NULL_VALUE,
                number=search_query,
                is_status_relevant=None
            ), 'avr'
        )
        current_path = urls.avr_claims_all
    return table, 'claims.html', current_path
