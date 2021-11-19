from .base import PaymentSystemABC


class UmoneySystem(PaymentSystemABC):
    async def process(self, data):

        return f"Перейдите по ссылке на Юмани, чтобы совершить оплату стоимостью {data['amount']} руб.\n(link)\nПодписка активируется автоматически."

    async def callback(self):
        
        return None