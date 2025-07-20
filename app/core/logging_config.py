LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "access": {
            "format": "%(asctime)s [%(levelname)s] %(client_addr)s - %(request_line)s - %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "admin_actions": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "shorturl_service": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
