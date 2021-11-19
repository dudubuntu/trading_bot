from aiogram.dispatcher.filters.state import StatesGroup, State

from .default import DefaultStates


class EducationStates(DefaultStates):
    parent = DefaultStates

    EducationDefaultState = State()
    EducationPaymentState = State()
    PaymentSystemState = State()


class EducationAboutStates(DefaultStates):
    AboutState = State()
