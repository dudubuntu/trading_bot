from aiogram import types
from data import config
from aiogram.dispatcher import Dispatcher
from sqlalchemy import select, insert, values, delete, update

from keyboards.default.default import DefaultKb
from utils.db.postgres.db import TgUser



async def bot_start(msg: types.Message):
    with await Dispatcher.get_current().data["db"] as conn:
        user = await (await conn.execute(select(TgUser).where(TgUser.chat_id == msg.from_user.id))).fetchone()
        if not user:
            await conn.execute(insert(TgUser, [{"chat_id": msg.from_user.id, "username": msg.from_user.username, "extra": dict(msg.from_user)}]))
    await msg.answer(text=f'Привет, {msg.from_user.full_name}!', reply_markup=DefaultKb().kb)
    
async def send_to_admin(dp, text):
    for admin_id in config.admins:
        await dp.bot.send_message(chat_id=admin_id, text=text)
