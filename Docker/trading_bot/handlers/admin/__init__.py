from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command

from handlers.user.base import BaseHandler
from .admin import AdminHandler
from states.admin.admin import AdminStates, AdminSignalStates, AdminAnswerStates
from filters.is_admin import AdminFilter


def setup(dp: Dispatcher):
    dp.register_message_handler(AdminHandler().default, Command("admin"), AdminFilter(True), state="*")

    dp.register_message_handler(BaseHandler().go_home, Text("На главную"), state="*")
    dp.register_message_handler(AdminHandler().go_back, Text("Назад"), state=AdminSignalStates)

    dp.register_message_handler(AdminHandler().signal, Text("Дать сигнал"), AdminFilter(True), state=AdminStates.AdminDefaultState)
    dp.register_message_handler(AdminHandler().signal_send, AdminFilter(True), state=AdminSignalStates.SignalDefaultState)
    
    dp.register_message_handler(AdminHandler().answer, Text("Ответить на вопрос"), AdminFilter(True), state=AdminStates.AdminDefaultState)
    dp.register_message_handler(AdminHandler().answer_send, AdminFilter(True), state=AdminAnswerStates.AnswerDefaultState)



