from typing import Optional

AVR_COLUMNS: list[str] = [
    "Номер", "Оператор", "Шифр опоры", "Внутренний шифр опоры TS", "ИО",
    "Макрорегион", "Регион", "Адрес", "Подразделение", "Дата возникновения",
    "Статус", "Актуальность статуса", "Дата обновления статуса"
]


def select_avr(
    null_value: str = 'NaN',
    limit: Optional[int] = 3000,
    number: Optional[str] = None,
    is_status_relevant: Optional[bool] = None,
    filter_power_supply: Optional[bool] = None
) -> str:
    """Этот запрос также используется для отправки данных в json формате."""

    # Условия для фильтрации по актуальности статуса
    if is_status_relevant is True:
        where_relevant_status_clause = (
            'AND s.is_status_relevant = true '
        )
    elif is_status_relevant is False:
        where_relevant_status_clause = (
            "AND s.is_status_relevant != true " +
            'AND cd.const_8 IS NOT NULL'
        )
    else:
        where_relevant_status_clause = 'AND cd.const_8 IS NOT NULL'

    # Условие для фильтрации по статусу
    where_status_clause = (
        "AND s.status = 'На резервном э/снaбжении' "
    ) if filter_power_supply else ''

    # Условие для фильтрации по номеру
    where_number_clause = (
        f"AND (tk.ticket LIKE '%{number}%' " +
        f"OR cd.const_4 LIKE '%{number}%')"
     ) if number else ''

    return (f'''
        SELECT {", ".join(f'"{column}"' for column in AVR_COLUMNS)} FROM (
        WITH constants_data AS (
            SELECT
                ticket_id,
                MAX(
                    CASE WHEN constant_type_id = 1 THEN constant_value END
                ) AS const_1,
                MAX(
                    CASE WHEN constant_type_id = 8 THEN constant_value END
                ) AS const_8,
                MAX(
                    CASE WHEN constant_type_id = 7 THEN constant_value END
                ) AS const_7,
                MAX(
                    CASE WHEN constant_type_id = 4 THEN constant_value END
                ) AS const_4,
                MAX(
                    CASE WHEN constant_type_id = 18 THEN constant_value END
                ) AS const_18,
                MAX(
                    CASE WHEN constant_type_id = 19 THEN constant_value END
                ) AS const_19
            FROM
                constants
            GROUP BY
                ticket_id
        )

        SELECT DISTINCT
            tk.ticket AS "Номер",
            COALESCE(cd.const_7, '{null_value}') AS "Оператор",
            COALESCE(cd.const_4, '{null_value}') AS "Шифр опоры",
            COALESCE(
                pl.site_id::text, '{null_value}'
            ) AS "Внутренний шифр опоры TS",
            COALESCE(pl.infrastructure_company, '{null_value}') AS "ИО",
            COALESCE(rg.macroregion, '{null_value}') AS "Макрорегион",
            COALESCE(cd.const_18, '{null_value}') AS "Регион",
            COALESCE(cd.const_19, '{null_value}') AS "Адрес",
            COALESCE(cd.const_1, '{null_value}') AS "Подразделение",
            COALESCE(cd.const_8, '{null_value}') AS "Дата возникновения",
            COALESCE(s.status, '{null_value}') AS "Статус",
            CASE
                WHEN s.is_status_relevant IS TRUE THEN 'актуальный'
                WHEN s.is_status_relevant IS FALSE THEN 'не актуальный'
                ELSE '{null_value}'
            END AS "Актуальность статуса",
            TO_CHAR(
                s.date_and_time, 'YYYY-MM-DD HH24:MI'
            ) AS "Дата обновления статуса",
            cd.const_8
        FROM
            tickets AS tk
        LEFT JOIN
            statuses AS s ON tk.ticket_id = s.ticket_id
        LEFT JOIN
            constants_data AS cd ON tk.ticket_id = cd.ticket_id
        LEFT JOIN
            poles AS pl ON cd.const_4 = pl.pole
        LEFT JOIN
            regions AS rg ON cd.const_18 = rg.region
        WHERE
            tk.ticket IS NOT NULL
            {where_number_clause}
            {where_relevant_status_clause}
            {where_status_clause}
        ORDER BY
            cd.const_8 DESC
        {'LIMIT ' + str(limit) if limit is not None else ''}
    ) AS avr;
    ''')
