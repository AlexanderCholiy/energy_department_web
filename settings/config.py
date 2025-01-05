import os

from dotenv import load_dotenv

CURRENT_DIR: str = os.path.dirname(os.path.abspath(__file__))
ENV_PATH: str = os.path.join(CURRENT_DIR, '.env')
load_dotenv(ENV_PATH)


class DBSet:
    """Параметры подключения к БД."""
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))
    DB_USER: str = os.getenv('DB_USER')
    DB_PSWD: str = os.getenv('DB_PSWD')
    DB_NAME_TECH_PRIS: str = os.getenv('DB_NAME_TECH_PRIS')
    DB_NAME_AVR: str = os.getenv('DB_NAME_AVR')
    DB_NAME_WEB: str = os.getenv('DB_NAME_WEB')


class WebSet:
    """Параметры подключения приложения и настройки безопасности."""
    WEB_HOST: str = os.getenv('WEB_HOST')
    WEB_PORT: int = int(os.getenv('WEB_PORT'))
    WEB_PREFIX: str = ''
    WEB_STATIC_URL: str = '/uptc-static'
    WEB_MIDDLEWARE_SECRET_KEY: str = os.getenv('WEB_MIDDLEWARE_SECRET_KEY')
    WEB_SECURITY_SECRET_KEY: str = os.getenv('WEB_SECURITY_SECRET_KEY')
    WEB_SECURITY_ALGORITHM: str = os.getenv('WEB_SECURITY_ALGORITHM')
    WEB_SECURITY_ACCESS_TOKEN_EXPIRE_SECONDS: int = int(
        os.getenv('WEB_SECURITY_ACCESS_TOKEN_EXPIRE_SECONDS')
    )


db_settings = DBSet()
web_settings = WebSet()
