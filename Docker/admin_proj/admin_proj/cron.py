from datetime import timedelta
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from django.db.models import F
import logging

from .models import *

level = logging.DEBUG
logfile = 'cron_job.log'
logging.basicConfig(level=level, filename = logfile)

logger = logging.getLogger(__name__)
debug = logger.debug
print = logger.info


class CheckSubscriptions(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 - 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron_updater_subscriptions'    # a unique code

    def do(self):
        result = Subscription.objects.update(is_active=False).where(created__gte=timezone.now() - timedelta(weeks=4 * F("rate")))
        print(result)