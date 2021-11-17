from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text

from .help import bot_help
from .start import bot_start
from .base import go_back
from .payment import payment_course, payment_subscription, choose_payment, payment_confirm, payment_finish
# from filters.base import BackFilter
# from filters.payments import BuyCourseFilter
from states.user.payment import PaymentStates


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())

    dp.register_message_handler(go_back, Text("Назад"), state="*")
    dp.register_message_handler(payment_course, Text("Купить курс"), state=None)
    dp.register_message_handler(payment_subscription, Text("Купить подписку"), state=None)
    dp.register_message_handler(payment_confirm, Text(equals=["Ю-Pay", "Telegram"]), state=PaymentStates.PaymentInitialized)
    dp.register_message_handler(choose_payment, state=PaymentStates.PaymentInitialized)
    dp.register_message_handler(payment_confirm, state=PaymentStates.PaymentChosen)
    dp.register_message_handler(payment_finish, state=PaymentStates.PaymentConfirmed)