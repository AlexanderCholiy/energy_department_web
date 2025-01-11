import os
import json
from typing import Dict, List, Callable, Tuple

from pandas import DataFrame
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from database.db_base import sql_queries
from database.requests.select_claims import select_claims, CLAIMS_COLUMNS
from database.requests.select_appeals import select_appeals, APPEALS_COLUMNS
from database.requests.select_avr import select_avr, AVR_COLUMNS
from settings.urls import urls

router = APIRouter()
templates = Jinja2Templates(
    directory=os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'templates', 'uptc'
    )
)

NULL_VALUE: str = 'NaN'

QUERY_CONFIG: Dict[str, Tuple[Callable, str, List[str]]] = {
    urls.uptc_api_claims: (select_claims, 'tech_pris', CLAIMS_COLUMNS),
    urls.uptc_api_appeals: (select_appeals, 'tech_pris', APPEALS_COLUMNS),
    urls.avr_api_claims: (select_avr, 'avr', AVR_COLUMNS),
}


@router.get(urls.uptc_api_claims)
@router.get(urls.uptc_api_appeals)
@router.get(urls.avr_api_claims)
async def handle_home_uptc(
    request: Request,
) -> JSONResponse:
    """Отправляем данные UPTC и AVR в json формате."""
    current_path = request.url.path
    query_func, database_name, columns = QUERY_CONFIG.get(
        current_path, (None, None, None)
    )

    if query_func is None:
        raise HTTPException(status_code=404, detail='Not found')

    limit = None
    data = sql_queries(query_func(
        null_value=NULL_VALUE, limit=limit), database_name
    )

    if not data or not data[0]:
        return JSONResponse(
            content={'message': 'No data'},
            status_code=status.HTTP_204_NO_CONTENT
        )

    df = DataFrame(data, columns=columns)

    try:
        json_content = df.to_json(orient='records')
        return JSONResponse(
            content=json.loads(json_content), status_code=status.HTTP_200_OK
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail='Error parsing data to json.'
        )
