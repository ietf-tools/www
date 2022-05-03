#!/bin/sh -e

python /app/manage.py migrate --no-input
python /app/manage.py createcachetable
python /app/manage.py collectstatic
python /app/manage.py test
python /app/manage.py makemigrations --check --no-input
