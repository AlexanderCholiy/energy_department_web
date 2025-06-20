import logging
import os
from contextlib import closing
from typing import List, Literal, Union

import psycopg2
from colorama import Fore, Style, init

from settings.config import db_settings  # noqa: E402

CURRENT_DIR: str = os.path.dirname(__file__)

init(autoreset=True)

LOG_DIR: str = os.path.join(CURRENT_DIR, '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'sql.log')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('sql_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s __ %(levelname)s __ %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def sql_queries(
    request: str, database: Literal['tech_pris', 'avr']
) -> Union[List, bool]:
    """
    Функция для выполнения запросов к базе данных PostgreSQL.

    Parameters:
    ----------
    - request : str
        SQL-запрос, который нужно выполнить.
    - database : Literal['tech_pris', 'avr']
        Имя базы данных, к которой будет выполнен запрос.
        Допустимые значения: 'tech_pris', 'avr'.

    Return:
    ------
    - list: Возвращает результаты запроса SELECT для запросов, не требующих
    COMMIT.
    - bool: Возвращает True для запросов, требующих выполнения COMMIT.
    - bool: Возвращает False в случае ошибки выполнения запроса.

    Raises:
    ------
    - ValueError:
        Если передано некорректное имя базы данных.

    - Exception: В случае возникновения ошибки при выполнении запроса
    результаты будут записаны в .log файл.
    """
    if database == 'tech_pris':
        database = db_settings.DB_NAME_TECH_PRIS
    elif database == 'avr':
        database = db_settings.DB_NAME_AVR
    else:
        raise ValueError('Некорректное имя БД.')

    try:
        with closing(psycopg2.connect(
            user=db_settings.DB_USER,
            password=db_settings.DB_PSWD,
            host=db_settings.DB_HOST,
            port=db_settings.DB_PORT,
            database=database
        )) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(request)

                if cursor.description:
                    results = cursor.fetchall()
                    return results
                else:
                    connection.commit()
                    return True

    except KeyboardInterrupt:
        raise

    except Exception as e:
        print(
            Fore.RED + Style.DIM +
            'В файле ' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            os.path.basename(__file__) +
            Style.RESET_ALL + Fore.RED + Style.DIM +
            ' произошла ошибка при выполнении запроса к БД:\n' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            request + '\n' +
            Style.RESET_ALL + str(e)
        )
        logger.error(
            f'\nВ файле {__file__} произошла ошибка ' +
            f'при выполнении запроса к БД:\n{request}\n{str(e)}'
        )

        return False
