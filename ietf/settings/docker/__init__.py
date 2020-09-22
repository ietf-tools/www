from typed_environment_configuration import (
    BoolVariable,
    StringVariable,
    StringListVariable,
    FillVars,
)
import dj_database_url

from ..base import *

_ENVVARS = [
    StringListVariable("ADDRESSES", default=""),  # list of allowed addresses
    StringVariable("APP_SECRET_KEY", prefix="APP_"),
    StringVariable("PROJECT"),  # Project namespace
    StringVariable(
        "ENVIRONMENT"
    ),  # Application environment i.e. development, production, etc.
    StringVariable("AWS_STORAGE_BUCKET_NAME", default=""),  # S3 Bucket Name
    StringVariable("AWS_S3_CUSTOM_DOMAIN", default=""),  # S3 Domain
    StringVariable("DATABASE_URL"),  # e.g. postgres URL
]

_DJANGO_ENVVARS = [
    BoolVariable("DJANGO_DEBUG", default=False),
    StringVariable("DJANGO_SERVER_ENV", default="Nonprod"),
]


FillVars(_ENVVARS, vars())
FillVars(_DJANGO_ENVVARS, vars(), "DJANGO_")
ALLOWED_HOSTS = ADDRESSES

DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
