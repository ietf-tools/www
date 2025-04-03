from django.apps import AppConfig


class UtilsAppConfig(AppConfig):
    name = "ietf.utils"
    verbose_name = "IETF Website Utils"

    def ready(self):
        from .signal_handlers import register_signal_handlers

        register_signal_handlers()
