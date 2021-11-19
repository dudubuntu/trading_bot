from abc import ABC, abstractmethod, abstractproperty
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from data import config

from utils.misc.logging import logger
from keyboards.default import DefaultKb


class Handler(ABC):
    states_class: StatesGroup = None

    @abstractmethod
    async def default(self, msg: types.Message, state: FSMContext):
        pass

    async def go_back(self, msg: types.Message, state: FSMContext):
        cur_state = await state.get_state()
        if cur_state == await self.states_class.first():
            await self.go_home(msg, state)
        else:
            await self.default(msg, state)


class BaseHandler(Handler):

    async def default(self, msg: types.Message, state: FSMContext):
        pass

    @staticmethod
    async def go_home(msg: types.Message, state: FSMContext):
        await state.finish()
        await msg.answer(text="Выберите команду", reply_markup=DefaultKb().kb)