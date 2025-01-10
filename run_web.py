import os

from colorama import Fore, Style, init
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

from app.common.log_timer import log_timer
from app.routes import authorization_routes
from app.routes import user_routes
from app.routes import api_routes
from app.routes.uptc import uptc_home_routes
from app.routes.uptc import uptc_details_routes
from app.routes.avr import avr_home_routes
from settings.config import web_settings
from settings.web_log_config import web_log_config

init(autoreset=True)

CURRENT_DIR: str = os.path.dirname(__file__)

app = FastAPI(debug=False, title='UPTC&AVR', version='1.1')
app.include_router(authorization_routes.router)
app.include_router(user_routes.router)
app.include_router(api_routes.router)
app.include_router(uptc_home_routes.router)
app.include_router(uptc_details_routes.router)
app.include_router(avr_home_routes.router)
app.mount(
    web_settings.WEB_STATIC_URL,
    StaticFiles(directory=os.path.join(CURRENT_DIR, 'static')),
    name='static',
)
app.add_middleware(
    SessionMiddleware, secret_key=web_settings.WEB_MIDDLEWARE_SECRET_KEY
)


@log_timer()
def start_server():
    workers = (os.cpu_count() * 2) + 1
    config = Config(
        app=app,
        host=web_settings.WEB_HOST,
        port=web_settings.WEB_PORT,
        workers=workers,
        reload=False,
        log_level='error',
        log_config=web_log_config,
    )
    server = Server(config)
    server.run()


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    script_name_without_extension = script_name.split('.')[0]

    print(
        Fore.MAGENTA + Style.BRIGHT +
        f'Запуск файла: {script_name_without_extension}\n'
        + Fore.CYAN + Style.DIM +
        'Для отладки запускайте приложение с помощью команды: '
        + Fore.WHITE + Style.DIM +
        f'python -m uvicorn {script_name_without_extension}:app --reload '
        f'--host {web_settings.WEB_HOST} --port {web_settings.WEB_PORT} ' +
        '--workers 1\n'
        + Fore.CYAN + Style.DIM + 'Сайт: '
        + Fore.WHITE + Style.DIM +
        f'{web_settings.WEB_HOST}:{web_settings.WEB_PORT}' +
        web_settings.WEB_PREFIX
    )

    try:
        start_server()
    except (KeyboardInterrupt, SystemExit):
        print(Fore.RED + 'Сервер остановлен.')
