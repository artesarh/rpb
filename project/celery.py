import os
from celery import Celery

app_env = os.getenv("APP_ENV", "prod")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"project.settings.{app_env}")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
