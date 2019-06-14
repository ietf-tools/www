#!/bin/bash

rm -rf /code/mod_wsgi-express-8001/regeneration
DJANGO_SETTINGS_MODULE=ietf.settings.production ./manage.py runmodwsgi --setup-only --port 8001 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8001/regeneration --log-directory /code/logs
echo "This directory is for comparison only. It is not used by the running server. It was created by "$0" at " `date` > /code/mod_wsgi-express-8001/regeneration/README
