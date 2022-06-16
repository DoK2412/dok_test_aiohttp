from aiohttp import web
import asyncpg
import os
from dotenv import load_dotenv
import logging.config  # подключение конфигурации логов


# подключение сборшика логера
from loggings.descriptionlogger import logger_config


load_dotenv()  # включение видисти env файла

logging.config.dictConfig(logger_config)  # получение собранного логера
log_info = logging.getLogger('app_info')  # активация логера инфо
log_error = logging.getLogger('app_error')  # активация логера ошибок


async def on_start(app):
    try:
        app['db'] = await asyncpg.connect(os.getenv("DATABASE_URL"))
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def on_closed(app):
    try:
        await app['db'].close()
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


async def make_app():
    from service.handler import Handler
    try:
        handler = Handler()
        app = web.Application()
        app.on_startup.append(on_start)  # запуск бд при старте
        app.add_routes([
            web.get('/', handler.handler_get_user),
            web.get('/{id}', handler.out_img),
            web.get('/info', handler.conclusion_log_info),
            web.get('/error', handler.conclusion_log_error),
            web.post('/registration', handler.handler_registration_user),
            web.post('/auth', handler.handler_auth_user),
            web.post('/img', handler.create_new_images),
        ])
        app.on_cleanup.append(on_closed)  # выключение бд при закрытии
        log_info.info('Программа запущена, база данных подключена,'
                      ' все готово к работе')
        return app
    except Exception:
        log_error.error('Получено исключение: ', exc_info=True)


if __name__ == '__main__':
    web.run_app(make_app())
