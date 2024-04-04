#!/bin/sh -e

set -x

pre-commit run --all-files
python /app/manage.py makemigrations --dry-run --no-input
python /app/manage.py makemigrations --check --no-input
python /app/manage.py migrate --no-input
python /app/manage.py createcachetable
python /app/manage.py collectstatic --no-input
pytest --cov --cov-report=xml
if [ -d /coverage ]; then cp .coverage coverage.xml /coverage/; fi
