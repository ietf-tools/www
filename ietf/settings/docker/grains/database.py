import dj_database_url

from .. import DATABASE_URL

DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
