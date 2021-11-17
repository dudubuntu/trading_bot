from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class BackFilter(BoundFilter):
    key = 'Назад'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        return True