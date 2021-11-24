from django.utils import timezone

from .celery import app
from .models import Subscription


app.conf.beat_schedule = {
    'check_subscriptions_dates': {
        'task': 'tasks.check_subscriptions_dates',
        'schedule': 60*60*24,
    },
}

app.conf.timezone = 'Europe/Moskow'


@app.task
def check_subscriptions_dates(arg):
    result = Subscription.objects.update(is_active=False).where(end_at__lt=timezone.now())
    return result