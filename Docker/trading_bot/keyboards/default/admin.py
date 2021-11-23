from .default import HomeKb


class AdminDefaultKb(HomeKb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            actions = [
                'Дать сигнал',
                'Ответить на вопрос'
            ],
            schema = [2],
            *args, **kwargs
        )