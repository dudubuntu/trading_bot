from aiogram.dispatcher.filters.state import StatesGroup, State


class PaymentStates(StatesGroup):

    PaymentInitialized = State()
    PaymentChosen = State()
    PaymentConfirmed = State()
    PaymentFinished = State()