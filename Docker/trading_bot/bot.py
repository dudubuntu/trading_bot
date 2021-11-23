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


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
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
    # await handlers.user.start.bot_start()

async def on_shutdown_temp(dp: Dispatcher):
    await db_helpers.close_pg(dp)


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = RedisStorage2(**config.redis)
    # dp = Dispatcher(bot, storage=storage)

    # web.run_app(init())

    from utils.misc import logging
    logging.setup()
    logger.info('Configure Webhook URL to: {url}', url=config.WEBHOOK_URL)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    handlers.user.setup(dp)
    handlers.admin.setup(dp)
    executor.start_polling(dp, on_startup=on_startup_temp, on_shutdown=on_shutdown_temp)

    # bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    # storage = RedisStorage2(**config.redis)
    # dp = Dispatcher(bot, storage=storage)

    # async def main():

    #     while True:
    #         db = await db_helpers.init_pg(dp, config)

    #         with await db as conn:
    #             print('Done')
    #         conn = await db.acquire()
    #         from sqlalchemy import select, insert, values, delete, update
    #         from utils.db.postgres.db import TgUser
    #         result = await conn.execute(insert(TgUser, [{"chat_id": 1, "username": "test"}]))
    #         print(result)
    #         result = await(await conn.execute(select(TgUser))).fetchall()
    #         print(result)
    #         await asyncio.sleep(10)
    #         conn.close()
    #         db.close()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())