from aiogram.dispatcher.filters.state import State

from states.default import DefaultStates


class AdminStates(DefaultStates):
    parent = DefaultStates

    AdminDefaultState = State()
    EducationPaymentState = State()


class AdminSignalStates(AdminStates):
    parent = AdminStates

    SignalDefaultState = State()


class AdminAnswerStates(AdminStates):
    parent = AdminStates

    AnswerDefaultState = State()