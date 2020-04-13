#!/bin/bash

rm -rf /code/mod_wsgi-express-8001/regeneration
DJANGO_SETTINGS_MODULE=ietf.settings.production ./manage.py runmodwsgi --setup-only --port 8001 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8001/regeneration --log-directory /code/logs --processes 50 --threads 5 --maximum-requests 10000 --request-timeout 120 --queue-timeout 90 --server-metrics --server-status
echo "This directory is for comparison only. It is not used by the running server. It was created by "$0" at " `date` > /code/mod_wsgi-express-8001/regeneration/README
