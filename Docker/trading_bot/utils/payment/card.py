from .base import PaymentSystemABC


class CardSystem(PaymentSystemABC):
    async def process(self, data):

        return f"Переведите сумму на банковские реквизиты ниже, чтобы совершить оплату стоимостью {data['amount']} руб.\n+79110185385"

    async def callback(self):
        
        return None