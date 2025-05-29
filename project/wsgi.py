"""
WSGI config for reporting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load .env file
load_dotenv()

# Get APP_ENV, default to 'prod' for WSGI
app_env = os.getenv("APP_ENV", "prod")

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"project.settings.{app_env}")

application = get_wsgi_application()
