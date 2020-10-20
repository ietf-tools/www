LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s | %(levelname)s [%(name)s.%(filename)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S%z",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["stdout"], "propagate": True, "level": "ERROR"},
        "core": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "accounts": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "shop": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "certificates": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "forms": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "elearning": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
        "shop_apps": {"handlers": ["stdout"], "propagate": True, "level": "INFO"},
    },
}
