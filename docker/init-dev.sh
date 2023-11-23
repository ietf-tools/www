#!/bin/sh -e

python /app/manage.py migrate --no-input
python /app/manage.py createcachetable
exec ./manage.py runserver 0:8000
