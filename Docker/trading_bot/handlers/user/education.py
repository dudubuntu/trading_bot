from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.sql.expression import insert, select

from .base import BaseHandler
from keyboards.default import HomeKb
from keyboards.default.education import EducationDefaultKb, AboutKb
from keyboards.default.payment import PaymentSystemKb
from states.user.education import EducationStates, EducationAboutStates
from utils.payment import education_prices, payment_systems, payment_types
from utils.misc.logging import logger
from utils.db.postgres.db import Post


class EducationHandler(BaseHandler):
    states_class = EducationStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.answer("Введите команду", reply_markup=EducationDefaultKb().kb)

    async def about(self, msg: types.Message, state: FSMContext):
        await EducationAboutStates.first()

        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "education_about"))).fetchone())["message"]
        await msg.answer(message, reply_markup=AboutKb().kb)

    async def payment_system(self, msg: types.Message, state: FSMContext):
        if await state.get_state() == EducationAboutStates.AboutState.state:
            await self.states_class.EducationPaymentState.set()
        else:
            await self.states_class.next()

        async with state.proxy() as data:
            data["education"] = {
                "amount": education_prices["default"],
            }

        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "education_price"))).fetchone())["message"]
        await msg.answer(message.format(amount=education_prices["default"]))

        await msg.answer("Выберите тип оплаты", reply_markup=PaymentSystemKb().kb)

    async def payment_process(self, msg: types.Message, state: FSMContext):
        await self.states_class.next()
        
        async with state.proxy() as data:
            data["education"] = {
                "system": msg.text,
                **data["education"]
            }

            message = await payment_systems[data["education"]["system"]]().process({"user_id": msg.from_user.id, "type": "education", **data["education"]})

        await msg.answer(message, reply_markup=HomeKb().kb)