import os
from celery import Celery
import logging

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_automation.settings.development')

app = Celery('gym_automation')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-subscription-reminders': {
        'task': 'apps.members.tasks.send_subscription_reminders',
        'schedule': 86400.0,  # Run daily (24 hours)
    },
    'send-motivational-emails': {
        'task': 'apps.members.tasks.send_motivational_emails',
        'schedule': 604800.0,  # Run weekly (7 days)
    },
    'send-birthday-wishes': {
        'task': 'apps.members.tasks.send_birthday_wishes',
        'schedule': 86400.0,  # Run daily
    },
    'send-inactivity-alerts': {
        'task': 'apps.members.tasks.send_inactivity_alerts',
        'schedule': 86400.0,  # Run daily
    },
}

app.conf.timezone = 'UTC'

logger = logging.getLogger(__name__)

@app.task(bind=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')