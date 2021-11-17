from collections import defaultdict

from .consts import DefaultConstructor


def get_default_kb(subscription_is_payed=None, course_is_payed=None):
    
    course_field = "Открыть курс" if course_is_payed else "Купить курс"
    subscription_field = "Продлить подписку" if subscription_is_payed else "Купить подписку"

    default_kb = DefaultConstructor._create_kb([
        course_field,
        subscription_field,
        "Помощь",
        "Личная консультация",
    ], [1, 1, 2])

    return default_kb

default_kb = DefaultConstructor._create_kb([
    "Купить курс",
    "Купить подписку",
    "Помощь",
    "Личная консультация",
], [1, 1, 2])

back_kb = DefaultConstructor._create_kb([
    "Назад"
], [1])