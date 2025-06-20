from typing import Optional

APPEALS_COLUMNS: list[str] = [
    "ID", "Номер обращения", "Дата статуса", "Статус", "Дата обновления",
    "Личный кабинет", "Балансодержатель", "Сетевая организация", "Филиал",
    "Дата обращения", "Ссылка на ЛК", "Тема обращения", "Текст обращения",
    "Адрес объекта", "Номер заявки", "Шифр опоры", "Внутренний шифр опоры"
]


def select_appeals(
    null_value: str = 'NaN',
    personal_area_id: list[int] = [1, 2, 3, 4, 5, 6],
    limit: Optional[int] = 20000,
    search_query: Optional[str] = None,
    appeal_id: Optional[int] = None,
    claim_number: Optional[int] = None,
    declarant_name: Optional[str] = None,
    personal_area_name: Optional[str] = None,
    detail: bool = False
) -> str:
    """Этот запрос также используется для отправки данных в json формате."""

    if search_query:
        where_clause_appeals = (f'''
            AND (
                CAST(ms.message_number AS TEXT) LIKE '%{search_query}%'
                OR const_1100.constant_text LIKE '%{search_query}%'
                OR const_1000.constant_text LIKE '%{search_query}%'
                OR const_2060.constant_text LIKE '%{search_query}%'
                OR const_1010.constant_text LIKE '%{search_query}%'
                OR const_1020.constant_text LIKE '%{search_query}%'
            )
        ''')
    elif appeal_id:
        where_clause_appeals = (
            f"AND ms.id = '{appeal_id}'"
        )
    elif claim_number and declarant_name and personal_area_name:
        where_clause_appeals = (
            f"AND const_2070.constant_text = '{claim_number}'" +
            f"\nAND d.name = '{declarant_name}'" +
            f"\nAND pa.name = '{personal_area_name}'"
        )
    else:
        where_clause_appeals = ''

    if detail:
        status_join = ('''
        LEFT JOIN
            messages_states AS st ON ms.id = st.message_id
        ''')
    else:
        status_join = ('''
        LEFT JOIN (
            SELECT DISTINCT ON (message_id) *
            FROM messages_states
            ORDER BY message_id, time_stamp DESC
        ) AS st ON ms.id = st.message_id
        ''')

    return (f'''
    SELECT
        main_table.*,
        ts.siteid AS "Внутренний шифр опоры"
    FROM (
    SELECT
        ms.id AS "ID",
        ms.message_number AS "Номер обращения",
        COALESCE(st.status_time, '{null_value}') AS "Дата статуса",
        COALESCE(st.message_status, '{null_value}') AS "Статус",
        TO_CHAR(st.time_stamp, 'YYYY-MM-DD HH24:MI') AS "Дата обновления",
        COALESCE(pa.name, '{null_value}') AS "Личный кабинет",
        COALESCE(d.name, '{null_value}') AS "Балансодержатель",
        COALESCE(
            const_1010.constant_text, '{null_value}'
        ) AS "Сетевая организация",
        COALESCE(const_1020.constant_text, '{null_value}') AS "Филиал",
        COALESCE(const_2030.constant_text, '{null_value}') AS "Дата обращения",
        COALESCE(
            const_1040.constant_text, pa.link, '{null_value}'
        ) AS "Ссылка на ЛК",
        COALESCE(const_2050.constant_text, '{null_value}') AS "Тема обращения",
        COALESCE(
            const_2060.constant_text, '{null_value}'
        ) AS "Текст обращения",
        COALESCE(const_1100.constant_text, '{null_value}') AS "Адрес объекта",
        COALESCE(const_2070.constant_text, '{null_value}') AS "Номер заявки",
        COALESCE(const_1000.constant_text, '{null_value}') AS "Шифр опоры"
    FROM
        messages AS ms
    {status_join}
    LEFT JOIN
        personal_areas AS pa ON ms.personal_area_id = pa.id
    LEFT JOIN
        declarant AS d ON ms.declarant_id = d.id
    LEFT JOIN
        messages_constants AS const_1010 ON const_1010.message_id = ms.id
        AND const_1010.constant_type = 1010
    LEFT JOIN
        messages_constants AS const_1020 ON const_1020.message_id = ms.id
        AND const_1020.constant_type = 1020
    LEFT JOIN
        messages_constants AS const_1040 ON const_1040.message_id = ms.id
        AND const_1040.constant_type = 1040
    LEFT JOIN
        messages_constants AS const_1100 ON const_1100.message_id = ms.id
        AND const_1100.constant_type = 1100
    LEFT JOIN
        messages_constants AS const_2030 ON const_2030.message_id = ms.id
        AND const_2030.constant_type = 2030
    LEFT JOIN
        messages_constants AS const_2050 ON const_2050.message_id = ms.id
        AND const_2050.constant_type = 2050
    LEFT JOIN
        messages_constants AS const_2060 ON const_2060.message_id = ms.id
        AND const_2060.constant_type = 2060
    LEFT JOIN
        messages_constants AS const_2070 ON const_2070.message_id = ms.id
        AND const_2070.constant_type = 2070
    LEFT JOIN
        messages_constants AS const_1000 ON const_1000.message_id = ms.id
        AND const_1000.constant_type = 1000
    WHERE
        ms.personal_area_id IN (
            {', '.join(map(str, personal_area_id))}
        )
        {where_clause_appeals}
    ) AS main_table
    LEFT JOIN
        towerstore AS ts ON main_table."Шифр опоры" = ts.ts_id
    ORDER BY
        "Дата обновления" DESC
    {'LIMIT ' + str(limit) if limit is not None else ''};
    ''')
