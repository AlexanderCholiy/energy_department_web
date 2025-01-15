from typing import Optional


def select_claims_and_appeals(
    null_value: str = 'NaN',
    number: Optional[str] = None,
    limit: Optional[int] = 10000
) -> str:
    where_clause_appeals = (
        f'WHERE CAST(ms.message_number AS TEXT) LIKE \'%{number}%\''
    ) if number else ''

    where_clause_claims = (
        f'WHERE CAST(cl.claim_number AS TEXT) LIKE \'%{number}%\''
    ) if number else ''

    return f'''
    SELECT
        'обращение' AS "Тип",
        ms.id AS "ID",
        ms.message_number AS "Номер",
        COALESCE(st.message_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(
            const_1040.constant_text, pa.link '{null_value}'
        ) AS "Ссылка на ЛК"
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
    {where_clause_appeals}

    UNION ALL

    SELECT
        'заявка' AS "Тип",
        cl.id AS "ID",
        cl.claim_number AS "Номер",
        COALESCE(st.claim_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(const_1040.constant_text, '{null_value}') AS "Ссылка на ЛК"
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
    {where_clause_claims}

    ORDER BY
        "Дата обновления" DESC
     {'LIMIT ' + str(limit) if limit is not None else ''};
    '''
