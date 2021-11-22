from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.user.base import BaseHandler
from keyboards.default.default import BackKb
from keyboards.default.admin import AdminDefaultKb
from states.admin.admin import AdminStates, AdminSignalStates

from utils.misc.logging import logger


class AdminHandler(BaseHandler):
    states_class = AdminStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.reply("Введите команду", reply_markup=AdminDefaultKb().kb)

    async def signal(self, msg: types.Message, state: FSMContext):
        await AdminSignalStates.first()
        await msg.reply("Отправьте сигнал в одном сообщении и он будет отослан всем юзерам, имеющим активную подписку.", reply_markup=BackKb().kb)

    async def signal_send(self, msg: types.Message, state: FSMContext):

        #Залить сигнал в базу
        #Отправить сигнал всем купившим подписку

        await msg.reply(f'Сигнал отправлен', reply_markup=BackKb().kb)