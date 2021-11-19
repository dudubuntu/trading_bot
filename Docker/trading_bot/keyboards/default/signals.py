from aiogram.types import ReplyKeyboardMarkup

from .consts import DefaultConstructor
from .default import BackKb


class SignalsDefaultKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'О платной группе',
                'Приобрести подписку'
            ],
            schema = [2],
            *args, **kwargs
        )


class AboutKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Приобрести подписку'
            ],
            schema = [1],
            *args, **kwargs
        )


class SubscriptionRatesKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                '1 мес',
                '3 мес',
                '6 мес',
            ],
            schema = [3],
            *args, **kwargs
        )


class PaymentSystemKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Юмани',
                'Карта',
            ],
            schema = [2],
            *args, **kwargs
        )