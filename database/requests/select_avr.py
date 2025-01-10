from typing import Optional

AVR_COLUMNS: list[str] = [
    "Номер", "Оператор", "Шифр опоры", "Внутренний шифр опоры TS", "ИО",
    "Макрорегион", "Регион", "Адрес", "Подразделение", "Дата возникновения",
    "Статус", "Актуальность статуса", "Дата обновления статуса"
]


def select_avr(
    null_value: str = 'NaN',
    limit: Optional[int] = 1000,
    number: Optional[str] = None,
    is_status_relevant: Optional[bool] = None,
    filter_power_supply: Optional[bool] = None
) -> str:
    """Этот запрос также используется для отправки данных в json формате."""

    where_relevant_status_clause = ''
    if is_status_relevant is not None:
        where_relevant_status_clause = (
            'AND s.is_status_relevant = ' + (
                'true' if is_status_relevant else 'false'
            )
        )

    where_status_clause = (
        "AND s.status = 'На резервном э/снaбжении' "
    ) if filter_power_supply else ''

    where_number_clause = f"AND tk.ticket LIKE '%{number}%'" if number else ''

    return (f'''
        SELECT
            tk.ticket AS "Номер",
            COALESCE(const_7.constant_value, '{null_value}') AS "Оператор",
            COALESCE(const_4.constant_value, '{null_value}') AS "Шифр опоры",
            COALESCE(
                pl.site_id::text, '{null_value}'
            ) AS "Внутренний шифр опоры TS",
            COALESCE(pl.infrastructure_company, '{null_value}') AS "ИО",
            COALESCE(rg.macroregion, '{null_value}') AS "Макрорегион",
            COALESCE(const_18.constant_value, '{null_value}') AS "Регион",
            COALESCE(const_19.constant_value, '{null_value}') AS "Адрес",
            COALESCE(const_1.constant_value, '{null_value}') AS "Подразделение",
            COALESCE(
                const_8.constant_value, '{null_value}'
            ) AS "Дата возникновения",
            COALESCE(s.status, '{null_value}') AS "Статус",
            CASE
                WHEN s.is_status_relevant = TRUE THEN 'актуальный'
                WHEN s.is_status_relevant = FALSE THEN 'не актуальный'
                ELSE '{null_value}'
            END AS "Актуальность статуса",
            TO_CHAR(
                s.date_and_time, 'YYYY-MM-DD HH24:MI'
            ) AS "Дата обновления статуса"
        FROM
            tickets AS tk
        LEFT JOIN
            statuses AS s ON tk.ticket_id = s.ticket_id
        LEFT JOIN
            constants AS const_1 ON tk.ticket_id = const_1.ticket_id
            AND const_1.constant_type_id = 1
        LEFT JOIN
            constants AS const_8 ON tk.ticket_id = const_8.ticket_id
            AND const_8.constant_type_id = 8
        LEFT JOIN
            constants AS const_7 ON tk.ticket_id = const_7.ticket_id
            AND const_7.constant_type_id = 7
        LEFT JOIN
            constants AS const_4 ON tk.ticket_id = const_4.ticket_id
            AND const_4.constant_type_id = 4
        LEFT JOIN
            constants AS const_18 ON tk.ticket_id = const_18.ticket_id
            AND const_18.constant_type_id = 18
        LEFT JOIN
            constants AS const_19 ON tk.ticket_id = const_19.ticket_id
            AND const_19.constant_type_id = 19
        LEFT JOIN
            constants AS const_23 ON tk.ticket_id = const_23.ticket_id
            AND const_23.constant_type_id = 23
        LEFT JOIN
            poles AS pl ON const_4.constant_value = pl.pole
        LEFT JOIN
            regions AS rg ON const_18.constant_value = rg.region
        WHERE
            tk.ticket IS NOT NULL
            {where_number_clause}
            {where_relevant_status_clause}
            {where_status_clause}
        ORDER BY
            s.date_and_time DESC
        {'LIMIT ' + str(limit) if limit is not None else ''};
    ''')
