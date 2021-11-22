from aiogram.dispatcher.filters.state import StatesGroup, State

from states.default import DefaultStates


class FeedbackStates(DefaultStates):
    parent = DefaultStates

    FeedbackDefaultState = State()