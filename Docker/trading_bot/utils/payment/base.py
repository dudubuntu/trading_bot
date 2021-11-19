from abc import ABC, abstractmethod


class PaymentSystemABC(ABC):

    @abstractmethod
    async def process(self, user_id, rate, amount, system):
        """Must return message to user"""
        raise 
    
    @abstractmethod
    async def callback(self):
        raise 