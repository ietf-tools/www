#!/bin/bash

echo "Running management commands..."
python manage.py collectstatic --no-input

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
