from aiogram import types
from data import config

from keyboards.default.default import DefaultKb
# from permissions import subscription_is_payed, course_is_payed


# async def bot_start(msg: types.Message):
#     reply_markup = get_default_kb(subscription_is_payed=subscription_is_payed(msg.from_user.id), 
#                                   course_is_payed=course_is_payed(msg.from_user.id))

#     await msg.answer(text=f'Привет, {msg.from_user.full_name}!', reply_markup=reply_markup)


async def bot_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}!', reply_markup=DefaultKb().kb)
    
async def send_to_admin(dp, text):
    for admin_id in config.admins:
        await dp.bot.send_message(chat_id=admin_id, text=text)
