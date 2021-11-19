from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.default import HomeKb

from .base import BaseHandler
from keyboards.default import DefaultKb
from states.user.feedback import FeedbackStates

from utils.misc.logging import logger


class FeedbackHandler(BaseHandler):
    states_class = FeedbackStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()
        await msg.reply("Отзыв 1\n....")
        await msg.reply("Отзыв 2\n....")
        await msg.reply("Отзыв 3\n....")
        await msg.reply("Отзыв 4\n....", reply_markup=HomeKb([], []).kb)