#!/bin/bash

echo "Running management commands..."
python /app/manage.py collectstatic --no-input

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
