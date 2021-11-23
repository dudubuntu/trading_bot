from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text

from .help import bot_help
from .start import bot_start
from .base import BaseHandler
from .signals import SignalsHandler
from states.user.signals import SignalsStates, AboutStates
from .education import EducationHandler
from states.user.education import EducationStates, EducationAboutStates
from .feedback import FeedbackHandler
from .question import QuestionHandler
from states.user.question import QuestionStates


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())

    dp.register_message_handler(BaseHandler().go_home, Text("На главную"), state="*")

    dp.register_message_handler(SignalsHandler().go_back, Text("Назад"), state=[AboutStates.AboutState, *SignalsStates.all_states])
    dp.register_message_handler(SignalsHandler().default, Text("Сигналы"), state=None)
    dp.register_message_handler(SignalsHandler().about, Text("О платной группе"), state=SignalsStates.SignalsDefaultState)
    dp.register_message_handler(SignalsHandler().subscription_rates, Text("Приобрести подписку"), state=[AboutStates.AboutState, SignalsStates.SignalsDefaultState])
    dp.register_message_handler(SignalsHandler().payment_system, state=SignalsStates.RatesState)
    dp.register_message_handler(SignalsHandler().payment_process, state=SignalsStates.PaymentSystemState)
    
    dp.register_message_handler(EducationHandler().go_back, Text("Назад"), state=[EducationAboutStates.AboutState, *EducationStates.all_states])
    dp.register_message_handler(EducationHandler().default, Text("Обучение"), state=None)
    dp.register_message_handler(EducationHandler().about, Text("Про обучение"), state=EducationStates.EducationDefaultState)
    dp.register_message_handler(EducationHandler().payment_system, Text("Приобрести обучение"), state=[EducationAboutStates.AboutState, EducationStates.EducationDefaultState])
    dp.register_message_handler(EducationHandler().payment_process, state=EducationStates.EducationPaymentState)

    dp.register_message_handler(FeedbackHandler().default, Text("Отзывы"), state=None)
    
    dp.register_message_handler(QuestionHandler().default, Text("Задать вопрос"), state=None)
    dp.register_message_handler(QuestionHandler().ls_question, Text("Спросить лично"), state=QuestionStates.QuestionDefaultState)
    dp.register_message_handler(QuestionHandler().bot_question, Text("Спросить в боте"), state=QuestionStates.QuestionDefaultState)
    dp.register_message_handler(QuestionHandler().post_question, state=QuestionStates.QuestionPostState)