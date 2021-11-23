from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.sql.expression import insert, select, update
from sqlalchemy.orm import aliased

from handlers.user.base import BaseHandler
from keyboards.default.default import BackKb
from keyboards.default.admin import AdminDefaultKb
from states.admin.admin import AdminStates, AdminSignalStates, AdminAnswerStates
from utils.misc.logging import logger
from utils.db.postgres.db import TgUser, Subscription


class AdminHandler(BaseHandler):
    states_class = AdminStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.answer("Введите команду", reply_markup=AdminDefaultKb().kb)

    async def signal(self, msg: types.Message, state: FSMContext):
        await AdminSignalStates.first()
        await msg.answer("Отправьте сигнал в одном сообщении и он будет отослан всем юзерам, имеющим активную подписку.", reply_markup=BackKb().kb)

    async def signal_send(self, msg: types.Message, state: FSMContext):
        dp = Dispatcher.get_current()

        with await dp.data["db"] as conn:

            users = [user[0] for user in (await (await conn.execute(
                select(TgUser.chat_id).where(
                    select(Subscription).where(Subscription.is_active == True).exists()
                )
            )).fetchall())]

        for user in users:
            await dp.bot.send_message(chat_id=user, text=msg.text)

        await msg.answer(f'Сигнал отправлен', reply_markup=BackKb().kb)
    
    async def answer(self, msg: types.Message, state: FSMContext):
        await AdminAnswerStates.first()
        await msg.answer("Выберите сообщение и ответьте на вопрос.", reply_markup=BackKb().kb)
    
    async def answer_send(self, msg: types.Message, state: FSMContext):
        reply_to_id = msg.reply_to_message["chat"]["id"]
        
        dp = Dispatcher.get_current()
        await dp.bot.send_message(chat_id=reply_to_id, text=msg.text)

        await msg.answer("Ответ отпрален", reply_markup=BackKb().kb)