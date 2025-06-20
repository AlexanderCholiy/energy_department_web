import os

from fastapi import (
    APIRouter, Depends, Form, HTTPException, Path, Request, status
)
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.common.check_authorization import check_authorization
from database.db_base import sql_queries
from database.db_users import get_db
from database.requests.select_appeals import select_appeals
from database.requests.select_claims import select_claims
from database.requests.select_pole_from_ts import select_pole_from_ts
from database.requests.update_claims_constants import update_claims_constants
from database.requests.update_messages_constants import (
    update_messages_constants
)
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
async def details_uptc(
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
                claim_id=number_id,
                detail=True
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
                appeal_id=number_id,
                detail=True
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


@router.post(urls.uptc_claims_all + '/{number_id}')
@router.post(urls.uptc_appeals_all + '/{number_id}')
async def update_details_uptc(
    request: Request,
    number_id: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    pole: str = Form('')
) -> Response:
    user, redirect_response = await check_authorization(request, db)
    if redirect_response:
        return redirect_response

    pole = pole.strip() if pole and len(pole) > 4 else None
    if not pole:
        return _redirect_with_message(
            request, 'Некорректный шифр опоры', 'error'
        )

    check_pole = sql_queries(select_pole_from_ts(pole), 'tech_pris')

    if not check_pole:
        return _redirect_with_message(
            request, f'Опора "{pole}" не найдена.', 'error'
        )

    if len(check_pole) > 1:
        return _redirect_with_message(
            request, f'Уточните шифр опоры "{pole}".', 'error'
        )

    if request.url.path.startswith(urls.uptc_claims_all):
        if not sql_queries(
            update_claims_constants(number_id, 1000, check_pole[0][0]),
            'tech_pris'
        ):
            return _redirect_with_message(
                request, 'Возникла ошибка при выполнении запроса.', 'error'
            )
    else:
        if not sql_queries(
            update_messages_constants(number_id, 1000, check_pole[0][0]),
            'tech_pris'
        ):
            return _redirect_with_message(
                request, 'Возникла ошибка при выполнении запроса.', 'error'
            )

    return _redirect_with_message(
        request, 'Данные успешно обновлены!', 'success'
    )


def _redirect_with_message(
    request: Request, message: str, message_type: str
) -> RedirectResponse:
    request.session['message'] = message
    request.session['message_type'] = message_type
    return RedirectResponse(
        url=request.headers.get('referer'),
        status_code=status.HTTP_303_SEE_OTHER
    )
