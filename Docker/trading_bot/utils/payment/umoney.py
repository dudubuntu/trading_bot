from aiogram.dispatcher import Dispatcher
from sqlalchemy.sql.expression import insert, select

from utils.db.postgres.db import Subscription

from .base import PaymentSystemABC
from utils.db.postgres.db import PaymentSystem, Invoice
from utils.db.postgres.utils import db_max_id
from utils.payment.config import subscription_rates_aliases, payment_types


class UmoneySystem(PaymentSystemABC):
    slug = "umoney"

    async def process(self, data):
        with await Dispatcher.get_current().data["db"] as conn:
            # async with conn.begin() as tr:
                # subscription = await conn.execute(insert(Subscription).values({"id": await db_max_id(conn, Subscription, max_plus_one=True),
                #                                                          "user": data["user_id"],
                #                                                          "rate": subscription_rates_aliases[data["rate"]]}))
                # # await conn.execute(insert(Invoice).values(id = await db_max_id(conn, Invoice, max_plus_one=True),
                # #                                     user = data["user_id"],
                # #                                     type = payment_types[data["type"]],
                # #                                     rate = subscription_rates_aliases[data["rate"]],
                # #                                     payment_system = self.slug,
                # #                                     subscription = subscription["id"]))

            message = (await (await conn.execute(select(PaymentSystem).where(PaymentSystem.slug == self.slug))).fetchone())["message"]
            return message.format(amount=data["amount"])

    async def callback(self):
        pass