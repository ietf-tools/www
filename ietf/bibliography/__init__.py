from django.apps import AppConfig


class BibliographyAppConfig(AppConfig):
    name = 'ietf.bibliography'
    verbose_name = "Bibliography items"


default_app_config = 'ietf.bibliography.BibliographyAppConfig'


# TODO:
# X bibliography item model with generic foreign key
#   item rendering method
# X model mixin with pre-parser method
#   item rendering template tag
#   itemS rendering template tag

