import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djconfig.settings')  # your main Django settings

app = Celery('djconfig')

# Read configuration from Django settings, using CELERY_ prefixed keys
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered Django apps
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True