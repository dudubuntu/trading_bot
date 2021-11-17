from .consts import DefaultConstructor


buy_course_kb = DefaultConstructor._create_kb([
    "Ю-Pay",
    "Telegram",
    "Назад"
], [2, 1])

buy_subscription_kb = DefaultConstructor._create_kb([
    "1 мес (10000р)",
    "3 мес (28000р)",
    "6 мес (50000р)",
    "Назад"
], [1, 1, 1, 1])

confirm_pay_kb = DefaultConstructor._create_kb([
    "Подтверждаю",
    "Назад"
], [1, 1])