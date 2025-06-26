"""
Django settings for reporting project.
...
"""

from datetime import timedelta
from pathlib import Path
import os
import environ
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))


DEBUG = env.bool("DEBUG", True)

TIME_ZONE = "UTC"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / f"{env.str("DB_PATH_APP", default="db/app.sqlite")}",
    },
    "api_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR
        / f"{env.str("DB_PATH_REPORTING", default="db/reporting.sqlite")}",
    },
    "reference_db": {
        "ENGINE": "django.db.backends.sqlite3",  # or your database type
        "NAME": BASE_DIR
        / f"{env.str("DB_PATH_REFEREBCE", default="db/reference.sqlite")}",
    },
}

DATABASE_ROUTERS = ["project.routers.ApiDatabaseRouter"]
# DATABASE_ROUTERS = []


# Quick-start development settings - unsuitable for production
SECRET_KEY = "django-insecure-zlz8%@#+fohc(io55wc%g(vp+*844+tjl%cekll+=6wozb3sk2"
ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    # "unfold",
    #  "unfold.contrib.filters",  # Optional: for special filters
    "rest_framework_simplejwt",
    "unfold.contrib.forms",  # Optional: for special form elements
    "django_seed",
    "schema_viewer",
    "drf_spectacular",
    "rest_framework",
    "django_filters",
    "django_celery_beat",
]

FIDELIS_APPS = [
    "api",
    "frontend",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + FIDELIS_APPS


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Ensure this is included
    ],
    "EXCEPTION_HANDLER": "api.exceptions.custom_drf_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Reporting API",
    "DESCRIPTION": "API for the Reporting project",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": False,
        "persistAuthorization": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "DEBUG": True,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom exposure management code to bubble exceptions
    "api.middleware.CustomDjangoExceptionMiddleware",
]

# CORS settings

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend/templates"],  # Add this line
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
APPEND_SLASH = True

# Static files
STATICFILES_DIRS = []  # Directory for your static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=36500),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=36500),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # Use your Django SECRET_KEY
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Celery Configuration
CELERY_BROKER_URL = "filesystem://"  # We'll use filesystem broker for simplicity
CELERY_RESULT_BACKEND = None  # We don't need to store results for backups
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

# Filesystem broker configuration
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "data_folder_in": BASE_DIR / "celery" / "queue",
    "data_folder_out": BASE_DIR / "celery" / "queue", 
    "data_folder_processed": BASE_DIR / "celery" / "processed",
}

# Celery Beat (Scheduler) Configuration
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Default periodic tasks
CELERY_BEAT_SCHEDULE = {
    'backup-databases-daily': {
        'task': 'project.tasks.run_db_backup',
        'schedule': 60.0 * 60.0 * 2,  # Every 2 hours (for testing - change to daily)
        # For daily at 2 AM: 'schedule': crontab(hour=2, minute=0),
        'options': {
            'expires': 3600,  # Task expires after 1 hour if not executed
        }
    },
    'test-celery-every-5-minutes': {
        'task': 'project.tasks.test_task',
        'schedule': 300.0,  # Every 5 minutes (for testing)
        'options': {
            'expires': 60,
        }
    },
}

# Worker configuration
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 50
