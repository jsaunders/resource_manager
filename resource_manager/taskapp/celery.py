
from __future__ import absolute_import
import os

import datetime
import pytz
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('resource_manager')


class CeleryConfig(AppConfig):
    name = 'resource_manager.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@periodic_task(run_every=(crontab(minute='*/1')))
def check_leases_ending():
    now = pytz.utc.localize(datetime.datetime.utcnow())
    from resource_manager.leases.models import Lease
    leases = Lease.objects.filter(active=True,end_time__lte=now)
    print(leases)
    for lease in leases:
        lease.resource.end_lease()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
