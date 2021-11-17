from aiogram import Dispatcher

from .is_admin import AdminFilter
from .base import BackFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    
    dp.filters_factory.bind(BackFilter)

