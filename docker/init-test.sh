#!/bin/sh -e

set -x

python /app/manage.py migrate --no-input
python /app/manage.py createcachetable
python /app/manage.py collectstatic --no-input
pytest --cov --cov-report=xml
if [ -d /coverage ]; then cp .coverage coverage.xml /coverage/; fi
python /app/manage.py makemigrations --dry-run --no-input
python /app/manage.py makemigrations --check --no-input
