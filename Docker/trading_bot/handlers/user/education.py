from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext

from .base import BaseHandler
from keyboards.default import HomeKb
from keyboards.default.education import EducationDefaultKb, AboutKb
from keyboards.default.payment import PaymentSystemKb
from states.user.education import EducationStates, EducationAboutStates
from utils.payment import education_prices, payment_systems

from utils.misc.logging import logger


class EducationHandler(BaseHandler):
    states_class = EducationStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.reply("Введите команду", reply_markup=EducationDefaultKb().kb)

    async def about(self, msg: types.Message, state: FSMContext):
        await EducationAboutStates.first()
        await msg.reply("О платной группе: \n...", reply_markup=AboutKb().kb)

    async def payment_system(self, msg: types.Message, state: FSMContext):
        if await state.get_state() == EducationAboutStates.AboutState.state:
            await self.states_class.EducationPaymentState.set()
        else:
            await self.states_class.next()

        async with state.proxy() as data:
            data["education"] = {
                "amount": education_prices["default"],
            }
        await msg.reply(f'Пост про стоимость\n{education_prices["default"]}')
        await msg.reply("Выберите тип оплаты", reply_markup=PaymentSystemKb().kb)

    async def payment_process(self, msg: types.Message, state: FSMContext):
        await self.states_class.next()
        
        async with state.proxy() as data:
            data["education"] = {
                "system": msg.text,
                **data["education"]
            }

            message = await payment_systems[data["education"]["system"]]().process({"user_id": msg.from_user.id, **data["education"]})

        await msg.reply(message, reply_markup=HomeKb().kb)