from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.default import HomeKb

from keyboards.default.question import QuestionDefaultKb
from keyboards.default.default import BackKb

from .base import BaseHandler
from states.user.question import QuestionStates

from utils.misc.logging import logger


class QuestionHandler(BaseHandler):
    states_class = QuestionStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.reply("Выберите команду", reply_markup=QuestionDefaultKb().kb)

    async def bot_question(self, msg: types.Message, state: FSMContext):
        await self.states_class.next()
        await msg.reply("Отправьте вопрос и я скоро на него отвечу", reply_markup=BackKb().kb)
    
    async def post_question(self, msg: types.Message, state: FSMContext):
        await state.finish()
        await msg.reply("Ваш вопрос был отправлен. Спасибо за фидбэк ;)", reply_markup=HomeKb().kb)