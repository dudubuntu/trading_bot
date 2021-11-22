from .default import HomeKb


class AdminDefaultKb(HomeKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Дать сигнал',
            ],
            schema = [1],
            *args, **kwargs
        )