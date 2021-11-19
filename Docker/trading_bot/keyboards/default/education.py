from aiogram.types import ReplyKeyboardMarkup

from .consts import DefaultConstructor
from .default import BackKb


class EducationDefaultKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Про обучение',
                'Приобрести обучение'
            ],
            schema = [2],
            *args, **kwargs
        )


class AboutKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Приобрести обучение'
            ],
            schema = [1],
            *args, **kwargs
        )