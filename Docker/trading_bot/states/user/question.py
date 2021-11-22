from aiogram.dispatcher.filters.state import State

from states.default import DefaultStates


class QuestionStates(DefaultStates):
    parent = DefaultStates

    QuestionDefaultState = State()
    QuestionPostState = State()