from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.sql.expression import insert, select

from .base import BaseHandler
from keyboards.default import HomeKb
from keyboards.default.signals import SignalsDefaultKb, AboutKb, SubscriptionRatesKb
from keyboards.default.payment import PaymentSystemKb
from states.user.signals import SignalsStates, AboutStates
from utils.payment import subscription_rates_prices, payment_systems, payment_types
from utils.misc.logging import logger
from utils.db.postgres.db import Post


class SignalsHandler(BaseHandler):
    states_class = SignalsStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.answer("Введите команду", reply_markup=SignalsDefaultKb().kb)

    async def about(self, msg: types.Message, state: FSMContext):
        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "signals_about"))).fetchone())["message"]

        await AboutStates.first()
        await msg.answer(message, reply_markup=AboutKb().kb)

    async def subscription_rates(self, msg: types.Message, state: FSMContext):
        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "signals_rates"))).fetchone())["message"]

        if await state.get_state() == AboutStates.AboutState.state:
            await self.states_class.RatesState.set()
        else:
            await self.states_class.next()

        await msg.answer(message, reply_markup=SubscriptionRatesKb().kb)
    
    async def payment_system(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["subscription"] = {
                "rate": msg.text,
                "amount": subscription_rates_prices[msg.text],
            }

        await self.states_class().next()
        await msg.answer("Выберите тип оплаты", reply_markup=PaymentSystemKb().kb)

    async def payment_process(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["subscription"] = {
                "system": msg.text,
                **data["subscription"]
            }

            message = await payment_systems[data["subscription"]["system"]]().process({"user_id": msg.from_user.id, "type": "subscription", **data["subscription"]})

        await msg.answer(message, reply_markup=HomeKb().kb)