import os
import json
from typing import Dict, List

from pandas import DataFrame
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from database.db_base import sql_queries
from database.requests.select_claims import select_claims, CLAIMS_COLUMNS
from database.requests.select_appeals import select_appeals, APPEALS_COLUMNS
from settings.urls import urls

router = APIRouter()
templates = Jinja2Templates(
    directory=os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'templates', 'uptc'
    )
)

PERSONAL_AREA: Dict[str, List[int]] = {
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


@router.get(urls.uptc_api_claims)
@router.get(urls.uptc_api_appeals)
async def handle_home_uptc(
    request: Request,
) -> JSONResponse:
    """Отправляем данные UPTC и AVR в json формате."""
    current_path = request.url.path
    if current_path == urls.uptc_api_claims:
        query_func = select_claims
        database_name = 'tech_pris'
        columns = CLAIMS_COLUMNS
    else:
        query_func = select_appeals
        database_name = 'tech_pris'
        columns = APPEALS_COLUMNS

    data = sql_queries(
        query_func(null_value=NULL_VALUE, limit=None), database_name
    )

    if not data or not data[0]:
        return JSONResponse(
            content={'message': 'No data'},
            status_code=status.HTTP_204_NO_CONTENT
        )

    df = DataFrame(data, columns=columns)

    json_data = df.to_json(orient='records')

    try:
        json_content = json.loads(json_data)
        return JSONResponse(
            content=json_content, status_code=status.HTTP_200_OK
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail='Error parsing data to json.'
        )
