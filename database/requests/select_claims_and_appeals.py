from typing import Optional


def select_claims_and_appeals(
    null_value: str = 'NaN',
    search_query: Optional[str] = None,
    limit: Optional[int] = 1000
) -> str:
    where_clause_appeals = (f'''
        WHERE
            CAST(ms.message_number AS TEXT) LIKE '%{search_query}%'
            OR const_1100.constant_text LIKE '%{search_query}%'
            OR const_1000.constant_text LIKE '%{search_query}%'
            OR const_2060.constant_text LIKE '%{search_query}%'
    ''') if search_query else ''

    where_clause_claims = (f'''
        WHERE
            CAST(cl.claim_number AS TEXT) LIKE '%{search_query}%'
            OR const_1100.constant_text LIKE '%{search_query}%'
            OR const_1000.constant_text LIKE '%{search_query}%'
            OR const_1090.constant_text LIKE '%{search_query}%'
    ''') if search_query else ''

    return f'''
    SELECT
        main_table.*,
        ts.siteid AS "Внутренний шифр опоры"
    FROM (
    SELECT
        'обращение' AS "Тип",
        ms.id AS "ID",
        ms.message_number AS "Номер",
        COALESCE(st.message_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(
            const_1040.constant_text, pa.link, '{null_value}'
        ) AS "Ссылка на ЛК",
        COALESCE(
            const_2030.constant_text, '{null_value}'
        ) AS "Дата",
        COALESCE(
            const_1100.constant_text, '{null_value}'
        ) AS "Адрес объекта",
        COALESCE(const_1000.constant_text, '{null_value}') AS "Шифр опоры"
    FROM
        messages AS ms
    LEFT JOIN (
        SELECT DISTINCT ON (message_id) *
        FROM messages_states
        ORDER BY message_id, time_stamp DESC
    ) AS st ON ms.id = st.message_id
    LEFT JOIN
        personal_areas AS pa ON ms.personal_area_id = pa.id
    LEFT JOIN
        declarant AS d ON ms.declarant_id = d.id
    LEFT JOIN
        messages_constants AS const_1040 ON const_1040.message_id = ms.id
        AND const_1040.constant_type = 1040
    LEFT JOIN
        messages_constants AS const_2030 ON const_2030.message_id = ms.id
        AND const_2030.constant_type = 2030
    LEFT JOIN
        messages_constants AS const_1100 ON const_1100.message_id = ms.id
        AND const_1100.constant_type = 1100
    LEFT JOIN
        messages_constants AS const_1000 ON const_1000.message_id = ms.id
        AND const_1000.constant_type = 1000
    LEFT JOIN
        messages_constants AS const_2060 ON const_2060.message_id = ms.id
        AND const_2060.constant_type = 2060
    {where_clause_appeals}
    ) AS main_table
    LEFT JOIN
        towerstore AS ts ON main_table."Шифр опоры" = ts.ts_id

    UNION ALL

    SELECT
        main_table.*,
        ts.siteid AS "Внутренний шифр опоры"
    FROM (
    SELECT
        'заявка' AS "Тип",
        cl.id AS "ID",
        cl.claim_number AS "Номер",
        COALESCE(st.claim_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(
            const_1040.constant_text, pa.link, '{null_value}'
        ) AS "Ссылка на ЛК",
        COALESCE(
            const_1030.constant_text, '{null_value}'
        ) AS "Дата",
        COALESCE(
            const_1100.constant_text, '{null_value}'
        ) AS "Адрес объекта",
        COALESCE(const_1000.constant_text, '{null_value}') AS "Шифр опоры"
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
        constants AS const_1040 ON const_1040.claim_id = cl.id
        AND const_1040.constant_type = 1040
    LEFT JOIN
        constants AS const_1030 ON const_1030.claim_id = cl.id
        AND const_1030.constant_type = 1030
    LEFT JOIN
        constants AS const_1100 ON const_1100.claim_id = cl.id
        AND const_1100.constant_type = 1100
    LEFT JOIN
        constants AS const_1000 ON const_1000.claim_id = cl.id
        AND const_1000.constant_type = 1000
    LEFT JOIN
        constants AS const_1090 ON const_1090.claim_id = cl.id
        AND const_1090.constant_type = 1090
    {where_clause_claims}
    ) AS main_table
    LEFT JOIN
        towerstore AS ts ON main_table."Шифр опоры" = ts.ts_id

    ORDER BY
        "Дата обновления" DESC
    {'LIMIT ' + str(limit) if limit is not None else ''};
    '''
