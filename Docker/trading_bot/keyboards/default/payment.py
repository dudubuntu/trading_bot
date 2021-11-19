from .default import BackKb


class PaymentSystemKb(BackKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Юмани',
                'Карта',
            ],
            schema = [2],
            *args, **kwargs
        )