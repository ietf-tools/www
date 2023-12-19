from django.apps import AppConfig

from .signal_handlers import register_signal_handlers


class UtilsAppConfig(AppConfig):
    name = 'ietf.utils'
    verbose_name = "IETF Website Utils"

    def ready(self):
        register_signal_handlers()
