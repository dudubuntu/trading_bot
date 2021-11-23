from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.sql.expression import insert, select

from keyboards.default.default import HomeKb
from .base import BaseHandler
from keyboards.default import DefaultKb
from states.user.feedback import FeedbackStates
from utils.misc.logging import logger
from utils.db.postgres.db import Post


class FeedbackHandler(BaseHandler):
    states_class = FeedbackStates

    async def default(self, msg: types.Message, state: FSMContext):
        await self.states_class.first()

        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(Post).where(Post.key == "feedback_list"))).fetchone())["message"]

        for review in message.strip().split("---"):
            await msg.answer(review, reply_markup=HomeKb([], []).kb)