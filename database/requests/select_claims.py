from typing import Optional

CLAIMS_COLUMNS: list[str] = [
    "ID", "Номер заявки", "Дата статуса", "Статус", "Дата обновления",
    "Личный кабинет", "Балансодержатель", "Дата заявки", "Ссылка на ЛК",
    "Комментарии", "Адрес объекта"
]


def select_claims(
    null_value: str = 'NaN',
    personal_area_id: list[int] = [1, 2, 3, 4, 5, 6],
    limit: Optional[int] = 1000,
    number: Optional[str] = None,
    claim_id: Optional[int] = None,
    claim_number: Optional[int] = None,
    declarant_name: Optional[str] = None,
    personal_area_name: Optional[str] = None
) -> str:
    """Этот запрос также используется для отправки данных в json формате."""

    if number:
        where_clause_claims = (
            "AND CAST(cl.claim_number AS TEXT) LIKE '%" + str(number) + "%'"
        )
    elif claim_id:
        where_clause_claims = (
            f"AND cl.id = '{claim_id}'"
        )
    elif claim_number and declarant_name and personal_area_name:
        where_clause_claims = (
            f"AND cl.claim_number = '{claim_number}'" +
            f"\nAND d.name = '{declarant_name}'" +
            f"\nAND pa.name = '{personal_area_name}'"
        )
    else:
        where_clause_claims = ''

    return (f'''
    SELECT
        cl.id AS "ID",
        cl.claim_number AS "Номер заявки",
        COALESCE(st.status_time, '{null_value}') AS "Дата статуса",
        COALESCE(st.claim_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(const_1030.constant_text, '{null_value}') AS "Дата заявки",
        COALESCE(const_1040.constant_text, '{null_value}') AS "Ссылка на ЛК",
        COALESCE(const_1090.constant_text, '{null_value}') AS "Комментарии",
        COALESCE(const_1100.constant_text, '{null_value}') AS "Адрес объекта"
    FROM
        claims AS cl
    LEFT JOIN (
        SELECT DISTINCT ON (claim_id) *
        FROM claims_states
        ORDER BY claim_id, time_stamp DESC
    ) AS st ON cl.id = st.claim_id
    LEFT JOIN
        personal_areas AS pa ON cl.personal_area_id = pa.id
    LEFT JOIN
        declarant AS d ON cl.declarant_id = d.id
    LEFT JOIN
        constants AS const_1030 ON const_1030.claim_id = cl.id
        AND const_1030.constant_type = 1030
    LEFT JOIN
        constants AS const_1040 ON const_1040.claim_id = cl.id
        AND const_1040.constant_type = 1040
    LEFT JOIN
        constants AS const_1090 ON const_1090.claim_id = cl.id
        AND const_1090.constant_type = 1090
    LEFT JOIN
        constants AS const_1100 ON const_1100.claim_id = cl.id
        AND const_1100.constant_type = 1100
    WHERE
        cl.personal_area_id IN (
            {', '.join(map(str, personal_area_id))}
        )
        {where_clause_claims}
    ORDER BY
        st.time_stamp DESC
    {'LIMIT ' + str(limit) if limit is not None else ''};
    ''')
