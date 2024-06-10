#!/bin/bash

echo "Running migrate..."
python /app/manage.py migrate --no-input

echo "Running collect static..."
python /app/manage.py collectstatic --no-input

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
