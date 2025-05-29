from .base import *

DEBUG = False
CORS_ALLOW_ALL_ORIGINS = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "api_errors.log",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "api": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
