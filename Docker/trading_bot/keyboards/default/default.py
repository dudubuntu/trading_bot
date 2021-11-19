from collections import defaultdict
from typing import Dict, List, OrderedDict, Union

from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup

from .consts import DefaultConstructor


# def get_default_kb(subscription_is_payed=None, course_is_payed=None):
    
#     course_field = "Открыть курс" if course_is_payed else "Купить курс"
#     subscription_field = "Продлить подписку" if subscription_is_payed else "Купить подписку"

#     default_kb = DefaultConstructor._create_kb([
#         course_field,
#         subscription_field,
#         "Помощь",
#         "Личная консультация",
#     ], [1, 1, 2])

#     return default_kb

class ButtonConstructor(DefaultConstructor):
    actions = []
    schema = []
    resize_keyboard = True
    selective = False
    one_time_keyboard = False

    def __init__(
            self,
            actions: List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]],
            schema: List[int]
    ):
        self.actions = actions + self.actions
        self.schema = schema + self.schema

        super().__init__()

    @property
    def kb(self) -> ReplyKeyboardMarkup:

        return self._create_kb(
            actions = self.actions,
            schema = self.schema,
            resize_keyboard = self.resize_keyboard,
            selective = self.selective,
            one_time_keyboard = self.one_time_keyboard
        )


class BackKb(ButtonConstructor):
    def __init__(
            self,
            actions: List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]]=[],
            schema: List[int]=[],
            *args, **kwargs
    ):
        super().__init__(
            actions = actions + ["Назад"],
            schema = schema + [1],
            *args, **kwargs
        )


class HomeKb(ButtonConstructor):
    def __init__(
            self,
            actions: List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]]=[],
            schema: List[int]=[],
            *args, **kwargs
    ):
        super().__init__(
            actions = actions + ["На главную"],
            schema = schema + [1],
            *args, **kwargs
        )


class DefaultKb(ButtonConstructor):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                "Сигналы",
                "Обучение",
                "Отзывы",
                "Задать вопрос",
            ],
            schema = [1, 1, 2],
            *args, **kwargs
        )