from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from utils.misc.logging import logger


class LoggingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self):
        super(LoggingMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: types.Message, data: dict):
        await logger.debug(f'{message} : {data}')