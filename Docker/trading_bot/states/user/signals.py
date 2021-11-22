from aiogram.dispatcher.filters.state import StatesGroup, State

from states.default import DefaultStates


class SignalsStates(DefaultStates):
    parent = DefaultStates

    SignalsDefaultState = State()
    RatesState = State()
    PaymentSystemState = State()


class AboutStates(DefaultStates):
    AboutState = State()