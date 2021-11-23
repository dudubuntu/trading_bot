from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.sql.expression import insert, select

from utils.db.postgres.db import Post
from keyboards.default.default import HomeKb
from keyboards.default.question import QuestionDefaultKb
from keyboards.default.default import BackKb
from .base import BaseHandler
from states.user.question import QuestionStates
from utils.misc.logging import logger
from data import config


class QuestionHandler(BaseHandler):
    states_class = QuestionStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.answer("Выберите команду", reply_markup=QuestionDefaultKb().kb)

    async def ls_question(self, msg: types.Message, state: FSMContext):
        await state.finish()
        
        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "question_contacts"))).fetchone())["message"]
        await msg.answer(message, reply_markup=HomeKb().kb)

    async def bot_question(self, msg: types.Message, state: FSMContext):
        await self.states_class.next()
        await msg.answer("Отправьте вопрос и я скоро на него отвечу", reply_markup=BackKb().kb)
    
    async def post_question(self, msg: types.Message, state: FSMContext):
        for admin_id in config.admins:
            message = f"@{msg.from_user.username} (id {msg.from_user.id}) задал вопрос:\n\n{msg.text}"
            await Dispatcher.get_current().bot.send_message(chat_id=admin_id, text=message)
        
        await state.finish()
        await msg.answer("Вопрос отправлен.", reply_markup=HomeKb().kb)