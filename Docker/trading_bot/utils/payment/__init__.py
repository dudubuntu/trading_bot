from .umoney import UmoneySystem
from .card import CardSystem


subscription_rates_prices = {
    "1 мес": 10000,
    "3 мес": 27000,
    "6 мес": 55000,
}

subscription_rates_aliases = {
    "1 мес": "1 месяц",
    "3 мес": "3 месяца",
    "6 мес": "6 месяцев",
}

education_prices = {
    "default": 10000,
}

payment_systems = {
    "Юмани": UmoneySystem,
    "Карта": CardSystem,
}