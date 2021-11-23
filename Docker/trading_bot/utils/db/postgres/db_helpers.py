import os
from aiopg.sa import create_engine
from aiogram.dispatcher import Dispatcher


async def init_pg(dp: Dispatcher, config: dict):

    engine = await create_engine(
        database = config.postgres_settings['POSTGRES_DB'],
        user = config.postgres_settings['POSTGRES_USER'],
        password = config.postgres_settings['POSTGRES_PASSWORD'],
        host = config.postgres_settings['POSTGRES_HOST'],
        port = config.postgres_settings['POSTGRES_PORT'],
        echo = True,
    )

    dp.data.update({"db": engine})
    # return engine


async def close_pg(dp: Dispatcher):
    dp.data["db"].close()
    await dp.data["db"].wait_closed()