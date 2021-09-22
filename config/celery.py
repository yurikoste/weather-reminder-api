import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email-every-3-minute': {
        'task': 'reminderAPI.tasks.send_beat_notification_3',
        'schedule': crontab(minute='*/180'),
    },
    'send-email-every-6-minute': {
        'task': 'reminderAPI.tasks.send_beat_notification_6',
        'schedule': crontab(minute='*/360'),
    },
    'send-email-every-12-minute': {
        'task': 'reminderAPI.tasks.send_beat_notification_12',
        'schedule': crontab(minute='*/720'),
    },
    'send-email-every-24-minute': {
        'task': 'reminderAPI.tasks.send_beat_notification_24',
        'schedule': crontab(minute='*/1440'),
    },
}
