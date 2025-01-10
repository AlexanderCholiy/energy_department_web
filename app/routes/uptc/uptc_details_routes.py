import os

from fastapi import APIRouter, Depends, Request, Form, Path, HTTPException
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.check_authorization import check_authorization
from database.db_users import get_db
from database.db_base import sql_queries
from database.requests.select_claims import select_claims
from database.requests.select_appeals import select_appeals
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


@router.get(urls.uptc_claims_all + '/{number_id}')
@router.get(urls.uptc_appeals_all + '/{number_id}')
async def handle_home_uptc(
    request: Request,
    number_id: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    search_query: str = Form('')
) -> Response:
    """Подробная информация по заявкам и обращениям."""

    user, redirect_response = await check_authorization(request, db)
    if redirect_response:
        return redirect_response

    current_path = request.url.path

    if current_path.startswith(urls.uptc_claims_all):
        template_name = 'claims_details.html'
        table_claims = sql_queries(
            select_claims(
                null_value=NULL_VALUE,
                claim_id=number_id
            ), 'tech_pris'
        )

        if not table_claims:
            raise HTTPException(status_code=404, detail='Заявка не найдена.')

        table_appeals = sql_queries(
            select_appeals(
                null_value=NULL_VALUE,
                claim_number=table_claims[0][1],
                declarant_name=table_claims[0][6],
                personal_area_name=table_claims[0][5]
            ), 'tech_pris'
        )
    else:
        template_name = 'appeals_details.html'
        table_appeals = sql_queries(
            select_appeals(
                null_value=NULL_VALUE,
                appeal_id=number_id
            ), 'tech_pris'
        )

        if not table_appeals:
            raise HTTPException(
                status_code=404, detail='Обращение не найдено.'
            )

        table_claims = sql_queries(
            select_claims(
                null_value=NULL_VALUE,
                claim_number=table_appeals[0][14],
                declarant_name=table_appeals[0][6],
                personal_area_name=table_appeals[0][5]
            ), 'tech_pris'
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
        'null_value': NULL_VALUE,
        'table_claims': table_claims,
        'table_appeals': table_appeals
    }

    return templates.TemplateResponse(template_name, context)
