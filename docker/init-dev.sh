#!/bin/sh -e

python /app/manage.py migrate --no-input
python /app/manage.py createcachetable
/usr/local/bin/gunicorn --config /app/docker/gunicorn.py --reload ietf.wsgi
