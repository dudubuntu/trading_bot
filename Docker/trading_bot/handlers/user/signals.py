from aiogram import types
from aiogram.dispatcher import FSMContext

from .base import BaseHandler
from keyboards.default import HomeKb
from keyboards.default.signals import SignalsDefaultKb, AboutKb, SubscriptionRatesKb
from keyboards.default.payment import PaymentSystemKb
from states.user.signals import SignalsStates, AboutStates
from utils.payment import subscription_rates_prices, payment_systems

from utils.misc.logging import logger


class SignalsHandler(BaseHandler):
    states_class = SignalsStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.reply("Введите команду", reply_markup=SignalsDefaultKb().kb)

    async def about(self, msg: types.Message, state: FSMContext):
        await AboutStates.first()
        await msg.reply("О платной группе: \n...", reply_markup=AboutKb().kb)

    async def subscription_rates(self, msg: types.Message, state: FSMContext):
        if await state.get_state() == AboutStates.AboutState.state:
            await self.states_class.RatesState.set()
        else:
            await self.states_class.next()

        await msg.reply("Выберите подписку", reply_markup=SubscriptionRatesKb().kb)
    
    async def payment_system(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["subscription"] = {
                "rate": msg.text,
                "amount": subscription_rates_prices[msg.text],
            }

        await self.states_class().next()
        await msg.reply("Выберите тип оплаты", reply_markup=PaymentSystemKb().kb)

    async def payment_process(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["subscription"] = {
                "system": msg.text,
                **data["subscription"]
            }

            message = await payment_systems[data["subscription"]["system"]]().process({"user_id": msg.from_user.id, **data["subscription"]})

        await msg.reply(message, reply_markup=HomeKb().kb)