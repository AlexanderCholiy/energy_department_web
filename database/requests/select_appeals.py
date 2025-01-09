from typing import Optional


def select_appeals(
    null_value: str = 'NaN',
    personal_area_id: list[int] = [1, 2, 3, 4, 5, 6],
    number: Optional[str] = None
) -> str:
    return (f'''
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
        COALESCE(const_1040.constant_text, '{null_value}') AS "Ссылка на ЛК",
        COALESCE(const_2050.constant_text, '{null_value}') AS "Тема обращения",
        COALESCE(
            const_2060.constant_text, '{null_value}'
        ) AS "Текст обращения",
        COALESCE(const_1100.constant_text, '{null_value}') AS "Адрес объекта"
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
    WHERE
        ms.personal_area_id IN (
            {', '.join(map(str, personal_area_id))}
        )
        {
            (
                "AND CAST(ms.message_number AS TEXT) LIKE '%" +
                str(number) + "%'"
            ) if number else ''}
    ORDER BY
        st.time_stamp DESC
    LIMIT 1000;
    ''')
