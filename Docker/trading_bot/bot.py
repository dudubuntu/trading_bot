import asyncio
from typing import List, Tuple

import aiojobs as aiojobs
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiohttp import web
from loguru import logger
import handlers

from data import config
from utils.db.postgres import db_helpers, db


# noinspection PyUnusedLocal
async def on_startup(app: web.Application):
    import middlewares
    import filters
    import handlers
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    handlers.user.setup(dp)
    logger.info('Configure Webhook URL to: {url}', url=config.WEBHOOK_URL)
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    await handlers.user.start.send_to_admin(dp, text="Сервер запущен")
    await db_helpers.init_pg(dp, config)


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
    await db_helpers.close_pg(dp)
    await app_bot.close()


async def init() -> web.Application:
    from utils.misc import logging
    import web_handlers
    logging.setup()
    scheduler = await aiojobs.create_scheduler()
    app = web.Application()
    subapps: List[Tuple[str, web.Application]] = [
        ('/tg/webhooks/', web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp['bot'] = bot
        subapp['dp'] = dp
        subapp['scheduler'] = scheduler
        app.add_subapp(prefix, subapp)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


async def on_startup_temp(dp: Dispatcher):
    await handlers.user.start.send_to_admin(dp, text="Сервер запущен")
    await db_helpers.init_pg(dp, config)

async def on_shutdown_temp(dp: Dispatcher):
    await db_helpers.close_pg(dp)


if __name__ == '__main__':
    # from utils.misc import logging
    # logging.setup()
    # logger.info('Configure Webhook URL to: {url}', url=config.WEBHOOK_URL)

    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = RedisStorage2(**config.redis)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    handlers.user.setup(dp)
    handlers.admin.setup(dp)
    executor.start_polling(dp, on_startup=on_startup_temp, on_shutdown=on_shutdown_temp)

    # TODO Поднять на application
    # web.run_app(init())
