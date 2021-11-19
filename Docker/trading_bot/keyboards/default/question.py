from aiogram.types import ReplyKeyboardMarkup

from .default import HomeKb


class QuestionDefaultKb(HomeKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Спросить лично',
                'Спросить в боте'
            ],
            schema = [2],
            *args, **kwargs
        )