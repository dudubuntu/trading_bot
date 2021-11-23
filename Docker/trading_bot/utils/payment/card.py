from aiogram.dispatcher import Dispatcher
from sqlalchemy.sql.expression import insert, select

from utils.db.postgres.db import Subscription

from .base import PaymentSystemABC
from utils.db.postgres.db import PaymentSystem, Invoice
from utils.db.postgres.utils import db_max_id
from utils.payment.config import subscription_rates_aliases, payment_types


class CardSystem(PaymentSystemABC):
    slug = "card"

    async def process(self, data):
        with await Dispatcher.get_current().data["db"] as conn:
            message = (await (await conn.execute(select(PaymentSystem).where(PaymentSystem.slug == self.slug))).fetchone())["message"]
            return message.format(amount=data["amount"])

    async def callback(self):
        
        return None