from aiogram import types
from aiogram.dispatcher import FSMContext
from data import config


from keyboards.default import default_kb


async def go_back(msg: types.Message, state: FSMContext):
    await state.reset_state()
    await msg.answer(text="Выберите команду", reply_markup=default_kb)